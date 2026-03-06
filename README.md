# Dhakar Samachar (PHP + Bootstrap Edition)

A Hostinger-friendly PHP news portal rebuilt from the previous Python stack.

## Highlights

- ✅ Pure **PHP** (no Python runtime needed)
- ✅ **Bootstrap 5** responsive UI with Bootstrap Icons
- ✅ Attractive **multi-color themes** (Sunset, Ocean, Forest)
- ✅ Built-in **multilanguage support** (English + Bangla)
- ✅ News home feed, details, search, shorts, e-paper list, legal pages

## Run locally

```bash
php -S 0.0.0.0:8000
```

Open `http://localhost:8000`.

## Project structure

- `index.php` — home + breaking ticker + latest cards
- `news.php` — single news detail page
- `search.php` — title/category search
- `shorts.php` — embedded video shorts page
- `epaper.php` — e-paper edition table
- `privacy.php`, `terms.php` — legal pages
- `includes/` — shared config, data, helpers, header/footer
- `assets/css/style.css` — theme + visual styling

## Hostinger deployment

1. Upload all project files to `public_html`.
2. Ensure PHP 8+ is enabled.
3. Set your domain root to this folder.
4. Done — no extra services required.

## Notes

Current demo content is in `includes/data.php`. Replace it with database-backed content later if needed.
