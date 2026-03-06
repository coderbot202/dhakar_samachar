# Dhakar Samachar - Dynamic News & Multimedia Portal

A Flask + Tailwind starter for a dynamic news platform with:

- Article publishing (with category + featured image)
- Shorts video uploads and vertical feed
- E-paper PDF archive (view/download)
- Breaking news ticker
- WhatsApp sharing button on article pages
- Comment submission + admin moderation
- Role-based admin panel (Admin, Publisher, Reporter)

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export SECRET_KEY="replace-with-a-strong-random-secret"
flask --app app init-db
flask --app app run
```

Open:
- Home: `http://127.0.0.1:5000/`
- Admin: `http://127.0.0.1:5000/admin`

Default admin credentials (change via env vars):
- `ADMIN_USERNAME=admin`
- `ADMIN_PASSWORD=admin123`


Environment requirements:
- `SECRET_KEY` must be set to a strong, non-default value. The app now fails fast if it is missing or set to `dev-secret-key`.

## Data model

### Category
- `id`, `name`, `slug`, timestamps

### News
- `id`, `title`, `summary`, `content`, `featured_image`, `is_breaking`, `category_id`, timestamps

### Shorts
- `id`, `caption`, `video_file`, timestamps

### PDFEdition
- `id`, `edition_date`, `pdf_file`, timestamps

### Comment
- `id`, `author_name`, `body`, `is_approved`, `news_id`, timestamps

## File uploads

Uploaded assets are stored under `uploads/`:
- `uploads/images`
- `uploads/videos`
- `uploads/pdfs`

## CI/CD

GitHub Actions runs tests for pull requests targeting `main`. On merges (pushes) to `main`, the workflow triggers production deployment by POSTing to `PRODUCTION_DEPLOY_WEBHOOK` (set this GitHub Actions secret in repository settings).

## Role access

- **Reporter**: upload news as draft only.
- **Publisher**: upload, edit, and publish reporter/publisher news, plus approve comments and upload shorts/e-paper.
- **Admin**: full control including categories, tags, tokens, UI-level controls via control panel forms.

## Legal pages

- `/privacy-policy`
- `/terms-and-conditions`


## Server deployment with automatic database setup

Yes — you can deploy directly to a server and let the app auto-create tables/seed defaults on first request.

Required env vars:
- `SECRET_KEY` (strong random value)
- `DATABASE_URL` (for production DB)

Optional:
- `AUTO_INIT_DB=true` (default enabled). Set to `false` if you want strict manual DB initialization only.

Example run:
```bash
export SECRET_KEY="your-strong-secret"
export DATABASE_URL="sqlite:////var/www/dhakar/news.db"
export AUTO_INIT_DB=true
gunicorn -w 2 -b 0.0.0.0:8000 app:app
```

You can still initialize manually anytime:
```bash
flask --app app init-db
```


## Production setup (fixing 403 Forbidden)

A plain **403 Forbidden** from the browser usually means the web server is serving static files only and your Flask app is not connected to a WSGI runner.

### 1) Required environment variables
- `SECRET_KEY` (must be strong and non-default)
- `DATABASE_URL` (recommended: MySQL/Postgres in production)
- `AUTO_INIT_DB=true` (optional; defaults to true)

### 2) Use a WSGI entrypoint
This repository now includes:
- `wsgi.py` for Gunicorn/systemd/Nginx
- `passenger_wsgi.py` for Passenger-style hosts (e.g., many cPanel/hPanel Python app setups)

### 3) Linux VPS (Nginx + Gunicorn + systemd)
Use these templates:
- `deployment/gunicorn.conf.py`
- `deployment/systemd.service.example`
- `deployment/nginx.conf.example`

Boot sequence:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export SECRET_KEY="your-strong-secret"
export DATABASE_URL="sqlite:////var/www/dhakar_samachar/news.db"
.venv/bin/gunicorn -c deployment/gunicorn.conf.py wsgi:application
```

### 4) Hostinger/hPanel style Python app
For exact click-by-click instructions after uploading code, use: `deployment/HOSTINGER_HPANEL_SETUP.md`.

- Set application startup file to `passenger_wsgi.py` (or WSGI module to `wsgi:application` if panel supports it).
- Ensure app root has read/execute permissions and `uploads/` is writable.
- Configure env vars in panel: `SECRET_KEY`, `DATABASE_URL`, `AUTO_INIT_DB`.
- Restart the Python app from panel.

### 5) Smoke test
After deploy, verify:
- `GET /health` returns `{"status":"ok"}`
- home page `/` loads (not 403)
