# Admin Panel Control Guide (Dhakar Samachar)

This guide explains how to control the admin panel in the current scaffold.

## 1) Who can access the admin panel?

Use role-based access control (RBAC) with these roles from Prisma:

- `SUPER_ADMIN`
- `ADMIN`
- `EDITOR`
- `JOURNALIST`
- `MODERATOR`

Recommended access policy:

- **SUPER_ADMIN**: full control of all admin modules and user roles
- **ADMIN**: operational control (articles, categories, ads, media, analytics)
- **EDITOR**: editorial control (articles, categories, tags, comments moderation)
- **JOURNALIST**: own article create/edit, no global settings
- **MODERATOR**: comments moderation only

## 2) How to control access technically

### Backend (source of truth)

Admin access should always be enforced on the backend using:

1. JWT authentication guard
2. Roles guard
3. Role decorators per route/module

Example route protection strategy:

- `GET /api/users` -> `SUPER_ADMIN`, `ADMIN`
- `POST /api/users/role` -> `SUPER_ADMIN` only
- `POST /api/articles` -> `EDITOR`, `JOURNALIST`, `ADMIN`, `SUPER_ADMIN`
- `POST /api/ads` -> `ADMIN`, `SUPER_ADMIN`
- `GET /api/analytics` -> `ADMIN`, `SUPER_ADMIN`

### Frontend (UX guard)

Frontend should mirror backend rules for user experience:

- Hide admin menu items if role does not allow them.
- Protect `/dashboard` and admin routes with middleware/session checks.
- Redirect unauthorized users to `/login` or a 403 page.

> Important: frontend checks improve UX, but **backend checks are mandatory** for security.

## 3) Day-to-day admin control workflow

1. **Create first SUPER_ADMIN** (seed script or DB insert).
2. Log in from admin login page.
3. Manage users and assign roles.
4. Review article workflow (`DRAFT -> REVIEW -> PUBLISHED/REJECTED`).
5. Manage homepage blocks, ads, and media.
6. Monitor analytics and comment moderation.

## 4) Emergency controls

If an account is compromised:

1. Change `JWT_SECRET` immediately.
2. Disable the user (`status = SUSPENDED` / `INACTIVE`).
3. Force re-login by invalidating refresh tokens.
4. Audit recent actions (article, ad, user-role updates).

## 5) Practical checklist

- [ ] JWT auth implemented for all protected APIs
- [ ] Roles guard enabled for admin modules
- [ ] User-role management endpoint restricted to SUPER_ADMIN
- [ ] Frontend route protection for `/dashboard/*`
- [ ] 403 unauthorized page present
- [ ] Audit logging for critical admin actions

---

If you want, next I can implement the actual code-level RBAC guards and protected admin routes end-to-end (backend + frontend middleware) in this repository.
