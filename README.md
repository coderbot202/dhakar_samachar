# Dhakar Samachar - Dynamic News & Multimedia Portal

A Flask + Tailwind starter for a dynamic news platform with:

- Article publishing (with category + featured image)
- Shorts video uploads and vertical feed
- E-paper PDF archive (view/download)
- Breaking news ticker
- WhatsApp sharing button on article pages
- Comment submission + admin moderation
- Simple admin authentication

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
flask --app app init-db
flask --app app run
```

Open:
- Home: `http://127.0.0.1:5000/`
- Admin: `http://127.0.0.1:5000/admin`

Default admin credentials (change via env vars):
- `ADMIN_USERNAME=admin`
- `ADMIN_PASSWORD=admin123`

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
