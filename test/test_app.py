import pytest
from sqlalchemy import text
from src.app import create_app


def run_sql_file(db, filepath):
    with open(filepath, "r") as file:
        sql = file.read()

    for statement in sql.split(";"):
        if statement.strip():
            db.session.execute(text(statement))

    db.session.commit()


@pytest.fixture
def app():
    app = create_app()
    db = app.config["DB"]

    with app.app_context():
        run_sql_file(db, "db/migration/001_create_todos.sql")
        run_sql_file(db, "db/seed/seed_todos.sql")

    yield app

    with app.app_context():
        db.session.execute(text("DROP TABLE IF EXISTS todos"))
        db.session.commit()


@pytest.fixture
def client(app):
    return app.test_client()


def test_index(client):
    response = client.get("/")
    assert response.data == b"Hello, World!"


def test_get_todos(client):
    response = client.get("/todos")
    todos = response.get_json()
    assert len(todos) > 0
