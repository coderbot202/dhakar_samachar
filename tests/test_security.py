import importlib
import os
import subprocess
import sys
import tempfile
import unittest
from io import BytesIO
from pathlib import Path


class SecretKeyImportTest(unittest.TestCase):
    def test_import_fails_without_secret_key(self):
        env = os.environ.copy()
        env.pop("SECRET_KEY", None)
        env.pop("DATABASE_URL", None)

        result = subprocess.run(
            [sys.executable, "-c", "import app"],
            capture_output=True,
            text=True,
            env=env,
            cwd=Path(__file__).resolve().parents[1],
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("SECRET_KEY environment variable", result.stderr)


class AppSecurityAndBootstrapTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.environ["SECRET_KEY"] = "test-secret-key"
        os.environ["AUTO_INIT_DB"] = "true"
        cls.db_fd, cls.db_path = tempfile.mkstemp(suffix=".db")
        os.environ["DATABASE_URL"] = f"sqlite:///{cls.db_path}"

        cls.app_module = importlib.import_module("app")
        cls.app_module.app.config.update(TESTING=True)

        cls.upload_tmp = tempfile.TemporaryDirectory()
        cls.app_module.UPLOAD_DIR = cls.upload_tmp.name
        cls.app_module.IMAGE_DIR = os.path.join(cls.upload_tmp.name, "images")
        cls.app_module.VIDEO_DIR = os.path.join(cls.upload_tmp.name, "videos")
        cls.app_module.PDF_DIR = os.path.join(cls.upload_tmp.name, "pdfs")
        os.makedirs(cls.app_module.IMAGE_DIR, exist_ok=True)
        os.makedirs(cls.app_module.VIDEO_DIR, exist_ok=True)
        os.makedirs(cls.app_module.PDF_DIR, exist_ok=True)

    @classmethod
    def tearDownClass(cls):
        cls.upload_tmp.cleanup()
        os.close(cls.db_fd)
        os.unlink(cls.db_path)

    def setUp(self):
        with self.app_module.app.app_context():
            self.app_module.db.drop_all()
            self.app_module.db.create_all()
        self.app_module.app.config["DB_BOOTSTRAPPED"] = False

    def test_invalid_edition_date_rejected_before_file_save(self):
        client = self.app_module.app.test_client()
        with client.session_transaction() as sess:
            sess["username"] = "admin"
            sess["role"] = self.app_module.ROLE_ADMIN

        response = client.post(
            "/admin/epaper",
            data={
                "edition_date": "../../etc/passwd",
                "pdf": (BytesIO(b"%PDF-1.4 fake"), "edition.pdf"),
            },
            content_type="multipart/form-data",
            follow_redirects=False,
        )

        self.assertEqual(response.status_code, 302)

        with self.app_module.app.app_context():
            count = self.app_module.PDFEdition.query.count()
        self.assertEqual(count, 0)

        pdf_files = list(Path(self.app_module.PDF_DIR).glob("*.pdf"))
        self.assertEqual(pdf_files, [])


    def test_health_endpoint_is_available(self):
        client = self.app_module.app.test_client()
        response = client.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'status': 'ok'})

    def test_auto_init_db_seeds_default_records_on_first_request(self):
        client = self.app_module.app.test_client()
        response = client.get("/", follow_redirects=False)
        self.assertEqual(response.status_code, 200)

        with self.app_module.app.app_context():
            self.assertGreaterEqual(self.app_module.Category.query.count(), 3)
            self.assertGreaterEqual(self.app_module.Tag.query.count(), 2)


if __name__ == "__main__":
    unittest.main()
