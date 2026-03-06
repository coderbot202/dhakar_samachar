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

ROLE_REPORTER = "reporter"
ROLE_PUBLISHER = "publisher"
ROLE_ADMIN = "admin"
ROLES = {ROLE_REPORTER, ROLE_PUBLISHER, ROLE_ADMIN}

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


class Tag(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    slug = db.Column(db.String(80), unique=True, nullable=False)


class APIToken(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    token_value = db.Column(db.String(255), nullable=False)


class News(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    summary = db.Column(db.String(512), nullable=False)
    content = db.Column(db.Text, nullable=False)
    featured_image = db.Column(db.String(255), nullable=True)
    is_breaking = db.Column(db.Boolean, default=False, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)
    status = db.Column(db.String(20), default="draft", nullable=False)
    author_username = db.Column(db.String(80), nullable=False)
    author_role = db.Column(db.String(20), nullable=False)
    tags = db.Column(db.String(255), default="", nullable=False)

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




def seed_default_data() -> None:
    if not Category.query.first():
        db.session.add_all(
            [
                Category(name="Local", slug="local"),
                Category(name="National", slug="national"),
                Category(name="Business", slug="business"),
            ]
        )
    if not Tag.query.first():
        db.session.add_all([Tag(name="Politics", slug="politics"), Tag(name="Sports", slug="sports")])
    db.session.commit()


def initialize_database() -> None:
    os.makedirs(IMAGE_DIR, exist_ok=True)
    os.makedirs(VIDEO_DIR, exist_ok=True)
    os.makedirs(PDF_DIR, exist_ok=True)
    db.create_all()
    seed_default_data()


def user_store() -> dict[str, tuple[str, str]]:
    return {
        os.getenv("REPORTER_USERNAME", "reporter"): (
            os.getenv("REPORTER_PASSWORD", "reporter123"),
            ROLE_REPORTER,
        ),
        os.getenv("PUBLISHER_USERNAME", "publisher"): (
            os.getenv("PUBLISHER_PASSWORD", "publisher123"),
            ROLE_PUBLISHER,
        ),
        os.getenv("ADMIN_USERNAME", "admin"): (
            os.getenv("ADMIN_PASSWORD", "admin123"),
            ROLE_ADMIN,
        ),
    }


def current_role() -> str | None:
    role = session.get("role")
    return role if role in ROLES else None


def can_manage_news(news_item: News) -> bool:
    role = current_role()
    username = session.get("username")
    if role == ROLE_ADMIN:
        return True
    if role == ROLE_PUBLISHER:
        return news_item.author_role in {ROLE_REPORTER, ROLE_PUBLISHER}
    return role == ROLE_REPORTER and news_item.author_username == username


def allowed_file(filename: str, allowed_extensions: set[str]) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions


def role_required(*roles: str):
    def decorator(view_func):
        @wraps(view_func)
        def wrapped(*args, **kwargs):
            role = current_role()
            if role not in roles:
                flash("You do not have access to this page.", "error")
                return redirect(url_for("admin_login"))
            return view_func(*args, **kwargs)

        return wrapped

    return decorator


@app.before_request
def ensure_database_initialized():
    if app.config.get("DB_BOOTSTRAPPED"):
        return

    if os.getenv("AUTO_INIT_DB", "true").lower() in {"1", "true", "yes"}:
        initialize_database()
        app.config["DB_BOOTSTRAPPED"] = True




@app.route("/health")
def health():
    return {"status": "ok"}, 200


@app.route("/")
def home():
    featured_news = (
        News.query.filter_by(status="published").order_by(News.created_at.desc()).limit(20).all()
    )
    breaking_news = (
        News.query.filter_by(status="published", is_breaking=True)
        .order_by(News.created_at.desc())
        .limit(10)
        .all()
    )
    return render_template("home.html", featured_news=featured_news, breaking_news=breaking_news)


@app.route("/privacy-policy")
def privacy_policy():
    return render_template("privacy_policy.html")


@app.route("/terms-and-conditions")
def terms_and_conditions():
    return render_template("terms_and_conditions.html")


@app.route("/news/<int:news_id>", methods=["GET", "POST"])
def news_detail(news_id: int):
    article = News.query.get_or_404(news_id)
    if article.status != "published":
        flash("This article is not published yet.", "error")
        return redirect(url_for("home"))

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
    query = request.args.get("q", "").strip()
    results = []
    if query:
        like_query = f"%{query}%"
        results = (
            News.query.filter(News.status == "published")
            .filter(
                (News.title.ilike(like_query))
                | (News.summary.ilike(like_query))
                | (News.content.ilike(like_query))
                | (News.tags.ilike(like_query))
            )
            .order_by(News.created_at.desc())
            .all()
        )
    return render_template("search.html", results=results, query=query)


@app.route("/uploads/<path:filename>")
def uploaded_file(filename: str):
    return send_from_directory(UPLOAD_DIR, filename)


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        users = user_store()
        user_record = users.get(username)
        if user_record and password == user_record[0]:
            session["username"] = username
            session["role"] = user_record[1]
            flash("Logged in successfully.", "success")
            return redirect(url_for("admin_dashboard"))
        flash("Invalid credentials.", "error")
    return render_template("admin_login.html")


@app.route("/admin/logout")
def admin_logout():
    session.pop("username", None)
    session.pop("role", None)
    flash("Logged out.", "success")
    return redirect(url_for("home"))


@app.route("/admin")
@role_required(ROLE_ADMIN, ROLE_PUBLISHER, ROLE_REPORTER)
def admin_dashboard():
    role = current_role()
    if role == ROLE_REPORTER:
        managed_news = News.query.filter_by(author_username=session.get("username")).order_by(News.created_at.desc()).all()
    else:
        managed_news = News.query.order_by(News.created_at.desc()).all()

    return render_template(
        "admin_dashboard.html",
        role=role,
        username=session.get("username"),
        categories=Category.query.order_by(Category.name.asc()).all(),
        tags=Tag.query.order_by(Tag.name.asc()).all(),
        tokens=APIToken.query.order_by(APIToken.created_at.desc()).all(),
        pending_comments=Comment.query.filter_by(is_approved=False).all(),
        managed_news=managed_news,
    )


@app.route("/admin/category", methods=["POST"])
@role_required(ROLE_ADMIN)
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


@app.route("/admin/tag", methods=["POST"])
@role_required(ROLE_ADMIN)
def add_tag():
    name = request.form.get("name", "").strip()
    slug = request.form.get("slug", "").strip().lower()
    if not name or not slug:
        flash("Tag name and slug are required.", "error")
        return redirect(url_for("admin_dashboard"))

    db.session.add(Tag(name=name, slug=slug))
    db.session.commit()
    flash("Tag added.", "success")
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/token", methods=["POST"])
@role_required(ROLE_ADMIN)
def add_token():
    name = request.form.get("name", "").strip()
    token_value = request.form.get("token_value", "").strip()
    if not name or not token_value:
        flash("Token name and value are required.", "error")
        return redirect(url_for("admin_dashboard"))

    db.session.add(APIToken(name=name, token_value=token_value))
    db.session.commit()
    flash("Token saved.", "success")
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/news", methods=["POST"])
@role_required(ROLE_ADMIN, ROLE_PUBLISHER, ROLE_REPORTER)
def add_news():
    title = request.form.get("title", "").strip()
    summary = request.form.get("summary", "").strip()
    content = request.form.get("content", "").strip()
    category_id = request.form.get("category_id")
    selected_tags = request.form.getlist("tags")
    featured_image = request.files.get("featured_image")

    image_path = None
    if featured_image and featured_image.filename:
        if not allowed_file(featured_image.filename, ALLOWED_IMAGE_EXTENSIONS):
            flash("Unsupported image format.", "error")
            return redirect(url_for("admin_dashboard"))
        filename = f"{int(datetime.utcnow().timestamp())}_{secure_filename(featured_image.filename)}"
        image_path = os.path.join("images", filename)
        featured_image.save(os.path.join(UPLOAD_DIR, image_path))

    role = current_role()
    status = "published" if role in {ROLE_ADMIN, ROLE_PUBLISHER} else "draft"

    news = News(
        title=title,
        summary=summary,
        content=content,
        category_id=int(category_id),
        featured_image=image_path,
        is_breaking=request.form.get("is_breaking") == "on" and role in {ROLE_ADMIN, ROLE_PUBLISHER},
        status=status,
        author_username=session.get("username", ""),
        author_role=role or ROLE_REPORTER,
        tags=",".join(selected_tags),
    )
    db.session.add(news)
    db.session.commit()
    flash("News article saved.", "success")
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/news/<int:news_id>/edit", methods=["POST"])
@role_required(ROLE_ADMIN, ROLE_PUBLISHER)
def edit_news(news_id: int):
    item = News.query.get_or_404(news_id)
    if not can_manage_news(item):
        flash("You cannot edit this article.", "error")
        return redirect(url_for("admin_dashboard"))

    item.title = request.form.get("title", "").strip()
    item.summary = request.form.get("summary", "").strip()
    item.content = request.form.get("content", "").strip()
    item.tags = ",".join(request.form.getlist("tags"))
    item.is_breaking = request.form.get("is_breaking") == "on"
    db.session.commit()
    flash("News updated.", "success")
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/news/<int:news_id>/publish", methods=["POST"])
@role_required(ROLE_ADMIN, ROLE_PUBLISHER)
def publish_news(news_id: int):
    item = News.query.get_or_404(news_id)
    if not can_manage_news(item):
        flash("You cannot publish this article.", "error")
        return redirect(url_for("admin_dashboard"))

    item.status = "published"
    db.session.commit()
    flash("News published.", "success")
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/shorts", methods=["POST"])
@role_required(ROLE_ADMIN, ROLE_PUBLISHER)
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
@role_required(ROLE_ADMIN, ROLE_PUBLISHER)
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
@role_required(ROLE_ADMIN, ROLE_PUBLISHER)
def approve_comment(comment_id: int):
    comment = Comment.query.get_or_404(comment_id)
    comment.is_approved = True
    db.session.commit()
    flash("Comment approved.", "success")
    return redirect(url_for("admin_dashboard"))


@app.cli.command("init-db")
def init_db_command():
    initialize_database()
    print("Database initialized.")


if __name__ == "__main__":
    with app.app_context():
        initialize_database()
    app.run(debug=True)
