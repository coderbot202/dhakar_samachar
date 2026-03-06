# Hostinger hPanel Production Setup (After Uploading Code)

Use this checklist after your project files are uploaded.

1. **Open hPanel → Advanced → Python** and create/select your Python app.
2. **Set Application Root** to your uploaded project folder (the folder containing `app.py`).
3. **Set Startup File** to `passenger_wsgi.py`.
4. **Set Python version** to 3.11+.
5. **Open Terminal in the same app root** and run:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
6. **Create writable upload directories**:
   ```bash
   mkdir -p uploads/images uploads/videos uploads/pdfs
   chmod -R 775 uploads
   ```
7. **Add Environment Variables in hPanel**:
   - `SECRET_KEY` = strong random secret (required)
   - `DATABASE_URL` = production DB URL (MySQL/Postgres preferred)
   - `AUTO_INIT_DB` = `true`
   - Optional role credentials:
     - `ADMIN_USERNAME`, `ADMIN_PASSWORD`
     - `PUBLISHER_USERNAME`, `PUBLISHER_PASSWORD`
     - `REPORTER_USERNAME`, `REPORTER_PASSWORD`
8. **Restart the Python application** from hPanel.
9. **Verify health endpoint** in browser:
   - `https://your-domain/health` should return JSON `{"status":"ok"}`.
10. **If still seeing 403**:
    - Confirm domain is mapped to Python app (not static site root).
    - Confirm startup file is exactly `passenger_wsgi.py`.
    - Confirm app root points to the same folder where `passenger_wsgi.py` exists.
    - Check hPanel Python logs for import/env errors.

## First login
- Visit: `https://your-domain/admin/login`
- Use configured credentials from environment variables.

