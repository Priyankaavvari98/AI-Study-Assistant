import os
os.environ.setdefault("GEMINI_API_KEY", "dummy-key-for-tests")

import pytest
import database
import app as app_module


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(
        database, "DATABASE", str(tmp_path / "test.db")
    )
    database.initialize_database()
    app_module.app.config["TESTING"] = True

    with app_module.app.test_client() as test_client:
        yield test_client