"""Role-Based Access Control (RBAC) and permissions system."""
from enum import Enum
from typing import Callable, Any
from functools import wraps
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.exceptions import AuthorizationError


class Role(str, Enum):
    """User roles with hierarchical permissions."""

    ANONYMOUS = "anonymous"  # Pre-auth session users
    USER = "user"  # Authenticated users
    MODERATOR = "moderator"  # Can moderate content, ban users
    ADMIN = "admin"  # Full system access
    BANNED = "banned"  # Blocked users


# Role hierarchy: higher roles inherit lower role permissions
ROLE_HIERARCHY = {
    Role.ADMIN: [Role.MODERATOR, Role.USER, Role.ANONYMOUS],
    Role.MODERATOR: [Role.USER, Role.ANONYMOUS],
    Role.USER: [Role.ANONYMOUS],
    Role.ANONYMOUS: [],
    Role.BANNED: [],
}


class Permission(str, Enum):
    """System permissions."""

    # User permissions
    USERS_LIST = "users.list"
    USERS_GET = "users.get"
    USERS_CREATE = "users.create"
    USERS_UPDATE = "users.update"
    USERS_DELETE = "users.delete"
    USERS_BAN = "users.ban"

    # Post permissions
    POSTS_LIST = "posts.list"
    POSTS_GET = "posts.get"
    POSTS_CREATE = "posts.create"
    POSTS_UPDATE = "posts.update"
    POSTS_UPDATE_ANY = "posts.update_any"
    POSTS_DELETE = "posts.delete"
    POSTS_DELETE_ANY = "posts.delete_any"

    # Admin permissions
    ADMIN_ACCESS = "admin.access"
    ANALYTICS_VIEW = "analytics.view"


# Permission mapping: role -> list of permissions
ROLE_PERMISSIONS: dict[Role, list[Permission]] = {
    Role.ANONYMOUS: [
        Permission.POSTS_LIST,
        Permission.POSTS_GET,
    ],
    Role.USER: [
        Permission.USERS_GET,
        Permission.USERS_UPDATE,
        Permission.POSTS_LIST,
        Permission.POSTS_GET,
        Permission.POSTS_CREATE,
        Permission.POSTS_UPDATE,
        Permission.POSTS_DELETE,
    ],
    Role.MODERATOR: [
        Permission.USERS_LIST,
        Permission.USERS_BAN,
        Permission.POSTS_UPDATE_ANY,
        Permission.POSTS_DELETE_ANY,
        Permission.ANALYTICS_VIEW,
    ],
    Role.ADMIN: [
        Permission.USERS_DELETE,
        Permission.ADMIN_ACCESS,
    ],
    Role.BANNED: [],
}


def get_user_permissions(role: Role) -> set[Permission]:
    """
    Get all permissions for a role including inherited permissions.

    Args:
        role: User role

    Returns:
        Set of permissions
    """
    permissions = set(ROLE_PERMISSIONS.get(role, []))

    # Add inherited permissions from role hierarchy
    inherited_roles = ROLE_HIERARCHY.get(role, [])
    for inherited_role in inherited_roles:
        permissions.update(ROLE_PERMISSIONS.get(inherited_role, []))

    return permissions


def has_permission(user_role: Role, permission: Permission) -> bool:
    """
    Check if role has specific permission.

    Args:
        user_role: User's role
        permission: Required permission

    Returns:
        True if user has permission
    """
    if user_role == Role.BANNED:
        return False

    user_permissions = get_user_permissions(user_role)
    return permission in user_permissions


def has_role(user_role: Role, required_role: Role) -> bool:
    """
    Check if user has required role or higher.

    Args:
        user_role: User's role
        required_role: Required role

    Returns:
        True if user has required role
    """
    if user_role == required_role:
        return True

    # Check if required role is in user's hierarchy
    inherited_roles = ROLE_HIERARCHY.get(user_role, [])
    return required_role in inherited_roles


def require_permission(
    permission: Permission,
    resource_check: Callable[..., Any] | None = None,
) -> Callable[..., Any]:
    """
    Decorator to require specific permission for endpoint.

    Args:
        permission: Required permission
        resource_check: Optional function to check resource-level permission

    Returns:
        Decorated function

    Example:
        ```python
        @require_permission(Permission.POSTS_UPDATE, check_post_owner)
        async def update_post(post_id: str, current_user: User):
            pass
        ```
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Get current_user from kwargs (injected by get_current_user dependency)
            current_user = kwargs.get("current_user")
            if not current_user:
                raise AuthorizationError("Authentication required")

            # Check if user is banned
            if current_user.role == Role.BANNED:
                raise AuthorizationError("User is banned")

            # Check permission
            if not has_permission(current_user.role, permission):
                raise AuthorizationError(
                    f"Missing required permission: {permission.value}",
                    details={"permission": permission.value},
                )

            # Check resource-level permission if provided
            if resource_check:
                db = kwargs.get("db")
                if not await resource_check(current_user, db, **kwargs):
                    raise AuthorizationError("Access denied to this resource")

            return await func(*args, **kwargs)

        return wrapper

    return decorator


def require_role(required_role: Role) -> Callable[..., Any]:
    """
    Decorator to require specific role for endpoint.

    Args:
        required_role: Minimum required role

    Returns:
        Decorated function

    Example:
        ```python
        @require_role(Role.MODERATOR)
        async def ban_user(user_id: str, current_user: User):
            pass
        ```
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            current_user = kwargs.get("current_user")
            if not current_user:
                raise AuthorizationError("Authentication required")

            if current_user.role == Role.BANNED:
                raise AuthorizationError("User is banned")

            if not has_role(current_user.role, required_role):
                raise AuthorizationError(
                    f"Required role: {required_role.value}",
                    details={"required_role": required_role.value},
                )

            return await func(*args, **kwargs)

        return wrapper

    return decorator


# Resource-level permission checkers
async def check_post_owner(current_user: Any, db: AsyncSession, **kwargs: Any) -> bool:
    """
    Check if current user owns the post or has moderator permissions.

    Args:
        current_user: Current authenticated user
        db: Database session
        **kwargs: Additional arguments (must contain post_id)

    Returns:
        True if user can access post
    """
    # Admins and moderators can access any post
    if has_role(current_user.role, Role.MODERATOR):
        return True

    # Regular users can only access their own posts
    post_id = kwargs.get("post_id")
    if not post_id:
        return False

    from app.models.post import Post
    from sqlalchemy import select

    result = await db.execute(select(Post).where(Post.id == post_id))
    post = result.scalar_one_or_none()

    if not post:
        return False

    return post.author_id == current_user.id


async def check_user_self_or_admin(current_user: Any, db: AsyncSession, **kwargs: Any) -> bool:
    """
    Check if current user is accessing their own data or is admin.

    Args:
        current_user: Current authenticated user
        db: Database session
        **kwargs: Additional arguments (must contain user_id)

    Returns:
        True if user can access data
    """
    # Admins can access any user
    if has_role(current_user.role, Role.ADMIN):
        return True

    # Users can only access their own data
    user_id = kwargs.get("user_id")
    return user_id == current_user.id
