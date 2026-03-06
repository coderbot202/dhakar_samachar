# Production Deployment Notice (dhakarsamachar.in)

If your current live website is running directly from `public_html` (shared hosting style), **do not upload this entire repository root to production**.

This repo now contains two different layers:

1. **Legacy live PHP site** at repository root (`index.php`, `news.php`, `includes/`, `assets/`, etc.)
2. **New monorepo scaffold** in subfolders:
   - `dhakar-samachar-frontend/` (Next.js)
   - `dhakar-samachar-backend/` (NestJS)
   - `docker-compose.yml`, `infra/`, `.github/`

Uploading everything blindly can break production routing and hosting expectations.

---

## Safe deployment options

## Option A: Keep current production stable (recommended now)

Upload **only** the PHP runtime files already used by your live site:

- `index.php`, `news.php`, `search.php`, `shorts.php`, `epaper.php`, `privacy.php`, `terms.php`
- `includes/`
- `assets/`

Do **not** upload:

- `dhakar-samachar-frontend/`
- `dhakar-samachar-backend/`
- `docker-compose.yml`
- `infra/`
- `.github/`

## Option B: Move to full-stack deployment (later)

Use VPS/container deployment for Next.js + NestJS + PostgreSQL + Redis + Elasticsearch + Nginx.
Shared hosting `public_html` alone is typically insufficient for this stack.

---

## Pre-deploy checklist for dhakarsamachar.in

- [ ] Confirm whether this deploy is **PHP-only** or **full-stack migration**
- [ ] Create backup of current `public_html`
- [ ] Upload only required files for chosen mode
- [ ] Verify homepage, article page, search, and legal pages
- [ ] Verify admin/login route after deploy

---

## Rollback plan

1. Keep a timestamped backup before every upload.
2. If issue appears, restore previous `public_html` backup immediately.
3. Re-test critical pages and DNS/SSL.

