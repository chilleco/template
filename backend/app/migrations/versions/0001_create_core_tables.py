"""Create core user and post tables

Revision ID: 0001
Revises: 
Create Date: 2024-05-08
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=320), nullable=True),
        sa.Column("phone", sa.String(length=32), nullable=True),
        sa.Column("username", sa.String(length=64), nullable=True),
        sa.Column("hashed_password", sa.Text(), nullable=True),
        sa.Column("password_salt", sa.LargeBinary(), nullable=True),
        sa.Column("role", sa.Enum("SUPERADMIN", "ADMIN", "EDITOR", "CREATOR", "USER", "RESTRICTED", name="userrole"), nullable=False, server_default="USER"),
        sa.Column("status", sa.Enum("ACTIVE", "PENDING", "BLOCKED", "DELETED", name="userstatus"), nullable=False, server_default="PENDING"),
        sa.Column("is_email_verified", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("is_phone_verified", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("profile", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("settings", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=False)
    op.create_index(op.f("ix_users_email_phone"), "users", ["email", "phone"], unique=False)
    op.create_index(op.f("ix_users_phone"), "users", ["phone"], unique=False)
    op.create_index(op.f("ix_users_username"), "users", ["username"], unique=False)

    op.create_table(
        "posts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("author_id", sa.Integer(), nullable=False),
        sa.Column("slug", sa.String(length=255), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("summary", sa.String(length=512), nullable=True),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("status", sa.Enum("DRAFT", "PUBLISHED", "ARCHIVED", name="poststatus"), nullable=False, server_default="DRAFT"),
        sa.Column("visibility", sa.Enum("PUBLIC", "PRIVATE", "UNLISTED", name="postvisibility"), nullable=False, server_default="PUBLIC"),
        sa.Column("locale", sa.String(length=10), nullable=False, server_default="en"),
        sa.Column("seo", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("extra", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("is_featured", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("published_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["author_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_posts_author_id"), "posts", ["author_id"], unique=False)
    op.create_index(op.f("ix_posts_slug"), "posts", ["slug"], unique=True)
    op.create_index(op.f("ix_posts_visibility_status"), "posts", ["visibility", "status"], unique=False)


    op.create_table(
        "user_login_activities",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("provider", sa.Enum("PASSWORD", "GOOGLE", "GITHUB", "APPLE", "TELEGRAM", "PHONE", name="authprovider"), nullable=False),
        sa.Column("ip_address", sa.String(length=64), nullable=True),
        sa.Column("user_agent", sa.String(length=255), nullable=True),
        sa.Column("metadata", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_user_login_activities_user_id"), "user_login_activities", ["user_id"], unique=False)


def downgrade() -> None:
    op.drop_table("user_login_activities")
    op.drop_table("posts")
    op.drop_table("users")
    op.execute("DROP TYPE IF EXISTS authprovider")
    op.execute("DROP TYPE IF EXISTS userrole")
    op.execute("DROP TYPE IF EXISTS userstatus")
    op.execute("DROP TYPE IF EXISTS poststatus")
    op.execute("DROP TYPE IF EXISTS postvisibility")
