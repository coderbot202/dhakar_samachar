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
