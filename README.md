# Dhakar Samachar - Dynamic News & Multimedia Portal

Flask + Tailwind implementation for a dynamic online news platform.

## Implemented modules

- **Dynamic News Engine**
  - Breaking ticker on homepage
  - Category-based news publishing
  - Rich content field (HTML-capable)
- **Multimedia**
  - Shorts feed with vertical snap-scrolling UI
  - E-Paper archive with view/download actions
- **Social + Engagement**
  - WhatsApp sharing link on article pages
  - Public comments with admin approval flow
- **Admin panel**
  - Login-protected dashboard
  - Upload News, Shorts, and PDF editions

## Local development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
flask --app app init-db
flask --app app run
```

## Production run

1. Copy `.env.example` to `.env` and set strong values.
2. Install dependencies and run with Gunicorn:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
gunicorn -w 3 -b 127.0.0.1:8000 wsgi:app
```

3. Install systemd service template from `deploy/dhakar-samachar.service`.

## CI/CD workflow (auto deploy on `main`)

GitHub Actions workflow: `.github/workflows/ci-cd.yml`

- On PR to `main`: installs dependencies and runs syntax validation.
- On push to `main`: **automatically deploys to production through SSH** after tests pass.
- Deployment does: pull latest `main` -> install deps -> run `flask init-db` -> restart service -> optional healthcheck.

### Required GitHub repository secrets

- `PROD_HOST`
- `PROD_USER`
- `PROD_SSH_KEY`
- `PROD_PORT`
- `PROD_APP_PATH` (example: `/var/www/dhakar_samachar`)
- `PROD_HEALTHCHECK_URL` (optional but recommended)

### One-time production server setup

```bash
cd /var/www
sudo git clone <your-repo-url> dhakar_samachar
cd dhakar_samachar
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# edit .env with production values
flask --app app init-db
sudo cp deploy/dhakar-samachar.service /etc/systemd/system/dhakar-samachar.service
sudo systemctl daemon-reload
sudo systemctl enable dhakar-samachar
sudo systemctl start dhakar-samachar
```

After this one-time setup, every push/merge to `main` auto-deploys and restarts the production service.

## Data model

- `Category`: `id`, `name`, `slug`, timestamps
- `News`: `id`, `title`, `summary`, `content`, `featured_image`, `is_breaking`, `category_id`, timestamps
- `Shorts`: `id`, `caption`, `video_file`, timestamps
- `PDFEdition`: `id`, `edition_date`, `pdf_file`, timestamps
- `Comment`: `id`, `author_name`, `body`, `is_approved`, `news_id`, timestamps

## File uploads

Uploaded assets are stored in:
- `uploads/images`
- `uploads/videos`
- `uploads/pdfs`
