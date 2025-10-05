# AI Code Generation Guidelines

This template is specifically designed for AI-assisted development (Claude Code, GitHub Copilot, etc.). Follow this workflow for consistent, high-quality code generation.

## Code Generation Workflow

### 1. Planning Phase
```
✓ Analyze requirements
✓ Review current repo structure
✓ Identify affected components
✓ Check localizations needed
✓ Verify access rules requirements
✓ Review styling patterns (shadcn/ui components)
✓ Check timezone handling needs
```

### 2. Backend Implementation

**Order:**
1. **Models & Migrations**
   ```bash
   # Generate model
   # Create Alembic migration
   alembic revision --autogenerate -m "description"
   ```

2. **Schemas (Pydantic)**
   - Request schemas
   - Response schemas
   - Validation rules

3. **Tests (Edge Cases)**
   - Generate comprehensive test cases
   - Cover all edge cases
   - Use fixtures from `tests/conftest.py`

4. **Services (Business Logic)**
   - Implement in `app/services/`
   - Keep routes thin
   - Extract reusable logic

5. **Routes (API Endpoints)**
   - POST-only JSON API
   - Use dependency injection
   - Apply authentication/permissions

6. **Complete Tests (100% Coverage)**
   ```bash
   pytest --cov=app --cov-report=term-missing
   ```

### 3. Documentation
- Docstrings for all functions
- OpenAPI descriptions
- Update API changelog

### 4. Frontend Implementation

**Order:**
1. **TypeScript Schemas**
   - Generate from Pydantic schemas
   - Place in `frontend/src/types/api/`

2. **API Client**
   - Add endpoints to `frontend/src/lib/api.ts`
   - Use type-safe methods

3. **Components**
   - Mobile-first design
   - Use shadcn/ui primitives
   - Support all themes
   - Add all localizations

4. **Pages**
   - SEO for public pages (Server Components)
   - Client Components for interactive parts
   - Implement access control

5. **State Management**
   - Add Redux slices if needed
   - Use React Query for server state

6. **Validation Checks**
   - ✓ Styling consistency
   - ✓ All locales present
   - ✓ Theme support (dark/light)
   - ✓ Access rules applied
   - ✓ Mobile responsive
   - ✓ Loading states
   - ✓ Error handling

7. **Frontend Tests**
   ```bash
   npm test
   ```

### 5. Final Steps
```bash
# Backend linting
cd backend
ruff check .
black .
mypy .

# Frontend linting
cd frontend
npm run lint
npm run type-check
```

## Project Conventions

### API Standards

**POST-only JSON API:**
```typescript
// All endpoints use POST with JSON body
POST /api/users.list
POST /api/users.get
POST /api/users.create
POST /api/users.update
POST /api/users.delete
```

**Request/Response Format:**
```python
# Request
{
    "user_id": "123",
    "filters": {...},
    "pagination": {"page": 1, "size": 20}
}

# Success Response
{
    "success": true,
    "data": {...},
    "meta": {...}
}

# Error Response
{
    "success": false,
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "Invalid input",
        "details": {...}
    }
}
```

### Error Handling

**Backend:**
```python
from app.core.exceptions import AppException

raise AppException(
    code="RESOURCE_NOT_FOUND",
    message="User not found",
    status_code=404,
    details={"user_id": user_id}
)
```

**Frontend:**
```typescript
try {
    await api.users.get({userId: '123'});
} catch (error) {
    if (error.code === 'RESOURCE_NOT_FOUND') {
        toast.error(t('errors.userNotFound'));
    }
}
```

### Authentication Flow

1. **Anonymous Session:**
   - Generate session token on first visit
   - Store anonymous actions (favorites, cart, etc.)

2. **Authentication:**
   - Support: email, phone, username, OAuth (Google, GitHub)
   - Merge anonymous session with user account
   - Return access + refresh tokens

3. **Token Management:**
   - Access token: 1 hour (JWT)
   - Refresh token: 30 days (stored in Redis)
   - Auto-refresh on expiry

### Permissions System

**Role-Based + Attribute-Based:**
```python
from app.core.permissions import require_permission

@require_permission("posts.edit", resource_check=check_post_owner)
async def update_post(post_id: str, current_user: User):
    # Implementation
    pass
```

**Roles:**
- `anonymous`: Pre-auth session users
- `user`: Authenticated users
- `moderator`: Can edit others' posts, ban users
- `admin`: Full access
- `banned`: Blocked users

### Localization

**Backend:**
```python
from app.core.i18n import get_translator

t = get_translator(locale)
message = t("errors.invalid_email")
```

**Frontend:**
```typescript
import { useTranslation } from '@/lib/i18n';

const { t } = useTranslation();
<p>{t('common.welcome')}</p>
```

**Supported Locales:**
- `en` (English) - default
- `ru` (Russian)
- `es` (Spanish)
- `zh` (Chinese)
- `ar` (Arabic)

### Timezone Handling

All times in UTC, convert on frontend:
```python
# Backend - always UTC
from datetime import datetime, timezone
created_at = datetime.now(timezone.utc)
```

```typescript
// Frontend - user's timezone
import { formatInTimeZone } from 'date-fns-tz';
const localTime = formatInTimeZone(date, userTimezone, 'PPpp');
```

### Component Patterns

**shadcn/ui Components:**
```bash
# Add new component
npx shadcn-ui@latest add button
```

**Component Structure:**
```typescript
// Mobile-first, theme-aware, accessible
import { cn } from '@/lib/utils';

export function MyComponent({ className, ...props }) {
    return (
        <div className={cn(
            "flex flex-col gap-4",        // Mobile first
            "md:flex-row md:gap-6",       // Desktop
            "dark:bg-slate-800",          // Dark theme
            className
        )}>
            {/* Content */}
        </div>
    );
}
```

### Background Tasks

**Task Types:**
```python
# 1. Scheduled (cron)
@task.schedule(cron="0 0 * * *")  # Daily at midnight
async def cleanup_old_sessions():
    pass

# 2. Event-driven (async callback)
@task.event("user.registered")
async def send_welcome_email(user_id: str):
    pass

# 3. Regular (continuous loop)
@task.regular(interval=60)  # Every 60 seconds
async def process_queue():
    pass
```

### Testing Patterns

**Backend:**
```python
# tests/api/test_users.py
async def test_create_user_success(client, db):
    response = await client.post("/api/users.create", json={
        "email": "test@example.com",
        "password": "SecurePass123!"
    })
    assert response.status_code == 200
    assert response.json()["success"] is True
```

**Frontend:**
```typescript
// tests/components/UserCard.test.tsx
import { render, screen } from '@testing-library/react';

test('renders user card', () => {
    render(<UserCard user={mockUser} />);
    expect(screen.getByText(mockUser.name)).toBeInTheDocument();
});
```

### Integration Clients

**Base Pattern:**
```python
# app/integrations/base.py - Raw API client
class StripeClient(BaseAPIClient):
    async def create_payment(self, amount: int) -> dict:
        return await self.post("/payments", {"amount": amount})

# app/services/payment.py - Unified service
class PaymentService:
    def __init__(self, provider: str = "stripe"):
        self.client = get_payment_client(provider)

    async def charge(self, amount: int, user_id: str) -> Payment:
        # Convert to internal format
        result = await self.client.create_payment(amount)
        return Payment.from_provider(result)
```

## File Naming Conventions

- **Backend:** `snake_case.py`
- **Frontend:** `PascalCase.tsx` (components), `camelCase.ts` (utils)
- **Tests:** `test_*.py`, `*.test.tsx`
- **Types:** `*.types.ts`

## Git Commit Messages

```
feat(users): add email verification
fix(auth): resolve token refresh race condition
test(posts): add edge cases for post creation
docs(api): update authentication endpoints
```

## Performance Considerations

1. **Database:**
   - Add indexes for frequently queried fields
   - Use `select_in_load` for relationships
   - Implement pagination everywhere

2. **Caching:**
   - Redis for session data
   - Cache expensive queries
   - Implement cache invalidation

3. **Frontend:**
   - Code splitting (dynamic imports)
   - Image optimization (Next.js Image)
   - Lazy load components

## Security Checklist

- [ ] Input validation (Pydantic)
- [ ] SQL injection prevention (SQLAlchemy ORM)
- [ ] XSS protection (React escaping)
- [ ] CSRF tokens (for cookies)
- [ ] Rate limiting
- [ ] Content Security Policy
- [ ] HTTPS only
- [ ] Secure headers (NGINX)

## AI Prompting Tips

**Good Prompt:**
> "Add a feature to allow users to save posts as favorites. Include:
> - Database model and migration
> - Backend API endpoints (list, add, remove favorites)
> - Frontend components with mobile-first design
> - All 5 localizations
> - Dark/light theme support
> - Full test coverage
> - Permission checks (only authenticated users)"

**Bad Prompt:**
> "Add favorites feature"

Always specify:
1. Full scope (backend + frontend)
2. Localization requirements
3. Theme support needs
4. Access control requirements
5. Test coverage expectations
6. Mobile responsiveness needs
