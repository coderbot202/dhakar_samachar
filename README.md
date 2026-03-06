# Dhakar Samachar Monorepo Scaffold

This repository now includes a production-focused scaffold for **Dhakar Samachar** with:

- **Next.js 14 frontend** (`dhakar-samachar-frontend`)
- **NestJS backend** (`dhakar-samachar-backend`)
- **Prisma PostgreSQL schema** for newsroom workflows
- **Docker Compose** stack (PostgreSQL, Redis, Elasticsearch, Nginx)
- **GitHub Actions CI** baseline

The legacy PHP prototype is still available at the repository root for reference.

## Architecture snapshot

- Frontend: App Router pages for public, admin, and auth route groups.
- Backend: Modular NestJS structure for auth, users, articles, categories, tags, comments, ads, media, analytics, and notifications.
- Data: Prisma models for users, articles, categories, tags, comments, ads, media, analytics, and homepage sections.

## Run with Docker

```bash
docker-compose up --build
```

- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:4000/api`
- Nginx gateway: `http://localhost`

## Next implementation milestones

1. Replace controller stubs with service-layer business logic.
2. Add JWT strategy, RBAC guards, and refresh token persistence.
3. Add Redis cache decorators for homepage and trending endpoints.
4. Add Elasticsearch indexing and query handlers.
5. Connect admin/editor UI to backend APIs with React Query.

## Admin panel control

See `ADMIN_PANEL_CONTROL.md` for role policy, access control flow, and operations checklist.
