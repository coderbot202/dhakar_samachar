import os
from datetime import datetime
from functools import wraps

from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    send_from_directory,
    session,
    url_for,
)
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
IMAGE_DIR = os.path.join(UPLOAD_DIR, "images")
VIDEO_DIR = os.path.join(UPLOAD_DIR, "videos")
PDF_DIR = os.path.join(UPLOAD_DIR, "pdfs")

ALLOWED_IMAGE_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}
ALLOWED_VIDEO_EXTENSIONS = {"mp4", "webm", "mov"}
ALLOWED_PDF_EXTENSIONS = {"pdf"}

app = Flask(__name__)
secret_key = os.getenv("SECRET_KEY")
if not secret_key or secret_key == "dev-secret-key":
    raise RuntimeError(
        "SECRET_KEY environment variable must be set to a strong, non-default value."
    )

app.config["SECRET_KEY"] = secret_key
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL", f"sqlite:///{os.path.join(BASE_DIR, 'news.db')}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["MAX_CONTENT_LENGTH"] = 200 * 1024 * 1024

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")

db = SQLAlchemy(app)


class TimestampMixin:
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )


class Category(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    slug = db.Column(db.String(80), unique=True, nullable=False)
    news = db.relationship("News", back_populates="category", lazy=True)


class News(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    summary = db.Column(db.String(512), nullable=False)
    content = db.Column(db.Text, nullable=False)
    featured_image = db.Column(db.String(255), nullable=True)
    is_breaking = db.Column(db.Boolean, default=False, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)

    category = db.relationship("Category", back_populates="news")
    comments = db.relationship(
        "Comment", back_populates="news", lazy=True, cascade="all,delete-orphan"
    )


class Shorts(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    caption = db.Column(db.String(255), nullable=False)
    video_file = db.Column(db.String(255), nullable=False)


class PDFEdition(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    edition_date = db.Column(db.Date, nullable=False, unique=True)
    pdf_file = db.Column(db.String(255), nullable=False)


class Comment(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_name = db.Column(db.String(120), nullable=False)
    body = db.Column(db.Text, nullable=False)
    is_approved = db.Column(db.Boolean, default=False, nullable=False)
    news_id = db.Column(db.Integer, db.ForeignKey("news.id"), nullable=False)

    news = db.relationship("News", back_populates="comments")


def allowed_file(filename: str, allowed_extensions: set[str]) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions


def admin_required(view_func):
    @wraps(view_func)
    def wrapped(*args, **kwargs):
        if not session.get("is_admin"):
            flash("Please login as admin.", "error")
            return redirect(url_for("admin_login"))
        return view_func(*args, **kwargs)

    return wrapped


@app.route("/")
def home():
    featured_news = News.query.order_by(News.created_at.desc()).limit(20).all()
    breaking_news = (
        News.query.filter_by(is_breaking=True).order_by(News.created_at.desc()).limit(10).all()
    )
    return render_template("home.html", featured_news=featured_news, breaking_news=breaking_news)


@app.route("/news/<int:news_id>", methods=["GET", "POST"])
def news_detail(news_id: int):
    article = News.query.get_or_404(news_id)

    if request.method == "POST":
        author_name = request.form.get("author_name", "").strip()
        body = request.form.get("body", "").strip()
        if author_name and body:
            db.session.add(Comment(author_name=author_name, body=body, news_id=article.id))
            db.session.commit()
            flash("Comment submitted for moderation.", "success")
        else:
            flash("Name and comment are required.", "error")
        return redirect(url_for("news_detail", news_id=news_id))

    approved_comments = Comment.query.filter_by(news_id=article.id, is_approved=True).all()
    return render_template(
        "news_detail.html", article=article, approved_comments=approved_comments
    )


@app.route("/shorts")
def shorts_feed():
    items = Shorts.query.order_by(Shorts.created_at.desc()).all()
    return render_template("shorts.html", shorts=items)


@app.route("/epaper")
def epaper_archive():
    editions = PDFEdition.query.order_by(PDFEdition.edition_date.desc()).all()
    return render_template("epaper.html", editions=editions)


@app.route("/search")
def search():
    q = request.args.get("q", "").strip()
    results = []
    if q:
        results = News.query.filter(
            db.or_(News.title.ilike(f"%{q}%"), News.summary.ilike(f"%{q}%"))
        ).order_by(News.created_at.desc())
    return render_template("search.html", q=q, results=results)


@app.route("/uploads/<path:filename>")
def uploaded_file(filename: str):
    return send_from_directory(UPLOAD_DIR, filename)


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["is_admin"] = True
            flash("Logged in successfully.", "success")
            return redirect(url_for("admin_dashboard"))
        flash("Invalid credentials.", "error")
    return render_template("admin_login.html")


@app.route("/admin/logout")
def admin_logout():
    session.pop("is_admin", None)
    flash("Logged out.", "success")
    return redirect(url_for("home"))


@app.route("/admin")
@admin_required
def admin_dashboard():
    return render_template(
        "admin_dashboard.html",
        categories=Category.query.order_by(Category.name.asc()).all(),
        pending_comments=Comment.query.filter_by(is_approved=False).all(),
    )


@app.route("/admin/category", methods=["POST"])
@admin_required
def add_category():
    name = request.form.get("name", "").strip()
    slug = request.form.get("slug", "").strip().lower()
    if not name or not slug:
        flash("Category name and slug are required.", "error")
        return redirect(url_for("admin_dashboard"))

    db.session.add(Category(name=name, slug=slug))
    db.session.commit()
    flash("Category added.", "success")
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/news", methods=["POST"])
@admin_required
def add_news():
    title = request.form.get("title", "").strip()
    summary = request.form.get("summary", "").strip()
    content = request.form.get("content", "").strip()
    category_id = request.form.get("category_id")
    is_breaking = request.form.get("is_breaking") == "on"
    featured_image = request.files.get("featured_image")

    image_path = None
    if featured_image and featured_image.filename:
        if not allowed_file(featured_image.filename, ALLOWED_IMAGE_EXTENSIONS):
            flash("Unsupported image format.", "error")
            return redirect(url_for("admin_dashboard"))
        filename = f"{int(datetime.utcnow().timestamp())}_{secure_filename(featured_image.filename)}"
        image_path = os.path.join("images", filename)
        featured_image.save(os.path.join(UPLOAD_DIR, image_path))

    news = News(
        title=title,
        summary=summary,
        content=content,
        category_id=int(category_id),
        featured_image=image_path,
        is_breaking=is_breaking,
    )
    db.session.add(news)
    db.session.commit()
    flash("News article created.", "success")
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/shorts", methods=["POST"])
@admin_required
def add_shorts():
    caption = request.form.get("caption", "").strip()
    video = request.files.get("video")

    if not video or not video.filename or not allowed_file(video.filename, ALLOWED_VIDEO_EXTENSIONS):
        flash("Valid video file is required.", "error")
        return redirect(url_for("admin_dashboard"))

    filename = f"{int(datetime.utcnow().timestamp())}_{secure_filename(video.filename)}"
    video_path = os.path.join("videos", filename)
    video.save(os.path.join(UPLOAD_DIR, video_path))

    db.session.add(Shorts(caption=caption, video_file=video_path))
    db.session.commit()
    flash("Short uploaded.", "success")
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/epaper", methods=["POST"])
@admin_required
def add_epaper():
    edition_date = request.form.get("edition_date", "").strip()
    pdf = request.files.get("pdf")

    if not pdf or not pdf.filename or not allowed_file(pdf.filename, ALLOWED_PDF_EXTENSIONS):
        flash("Valid PDF file is required.", "error")
        return redirect(url_for("admin_dashboard"))

    try:
        edition_date_obj = datetime.strptime(edition_date, "%Y-%m-%d").date()
    except ValueError:
        flash("Edition date must be in YYYY-MM-DD format.", "error")
        return redirect(url_for("admin_dashboard"))

    safe_edition_date = edition_date_obj.isoformat()
    filename = f"{safe_edition_date}_{secure_filename(pdf.filename)}"
    pdf_path = os.path.join("pdfs", filename)
    pdf.save(os.path.join(UPLOAD_DIR, pdf_path))

    db.session.add(PDFEdition(edition_date=edition_date_obj, pdf_file=pdf_path))
    db.session.commit()
    flash("E-paper uploaded.", "success")
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/comment/<int:comment_id>/approve", methods=["POST"])
@admin_required
def approve_comment(comment_id: int):
    comment = Comment.query.get_or_404(comment_id)
    comment.is_approved = True
    db.session.commit()
    flash("Comment approved.", "success")
    return redirect(url_for("admin_dashboard"))


@app.cli.command("init-db")
def init_db_command():
    os.makedirs(IMAGE_DIR, exist_ok=True)
    os.makedirs(VIDEO_DIR, exist_ok=True)
    os.makedirs(PDF_DIR, exist_ok=True)
    db.create_all()

    if not Category.query.first():
        seeds = [
            Category(name="Local", slug="local"),
            Category(name="National", slug="national"),
            Category(name="Business", slug="business"),
        ]
        db.session.add_all(seeds)
        db.session.commit()

    print("Database initialized.")


if __name__ == "__main__":
    os.makedirs(IMAGE_DIR, exist_ok=True)
    os.makedirs(VIDEO_DIR, exist_ok=True)
    os.makedirs(PDF_DIR, exist_ok=True)
    with app.app_context():
        db.create_all()
    app.run(debug=True)
