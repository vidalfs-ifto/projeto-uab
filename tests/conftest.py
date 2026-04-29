import pytest
from app import create_app
from app.database import db
from app.models.usuario_model import UsuarioModel

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SECRET_KEY": "test_secret",
        "WTF_CSRF_ENABLED": False
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

@pytest.fixture
def init_database(app):
    # Criar um proprietário inicial para testes
    with app.app_context():
        u = UsuarioModel(nome="Admin", email="admin@test.com", role="PROPRIETARIO")
        u.set_senha("password")
        db.session.add(u)
        db.session.commit()
        yield db
