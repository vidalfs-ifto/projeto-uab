import pytest
from app.models.usuario_model import UsuarioModel

def test_login_sucesso(client, init_database):
    # CT-01: Login Sucesso
    response = client.post("/login", data={
        "email": "admin@test.com",
        "senha": "password"
    }, follow_redirects=True)
    assert response.status_code == 200
    assert "dashboard" in response.request.path.lower() or b"Dashboard" in response.data

def test_login_falha(client, init_database):
    # CT-02: Login Falha
    response = client.post("/login", data={
        "email": "admin@test.com",
        "senha": "wrongpassword"
    }, follow_redirects=True)
    assert "erro=credenciais" in response.request.url.lower()

def test_register_cliente(client, app):
    # Teste de registro de cliente
    response = client.post("/register", data={
        "nome": "Novo Cliente",
        "email": "cliente@test.com",
        "senha": "password123"
    }, follow_redirects=True)
    assert response.status_code == 200
    
    with app.app_context():
        usuario = UsuarioModel.query.filter_by(email="cliente@test.com").first()
        assert usuario is not None
        assert usuario.role == "CLIENTE"

def test_oauth_google_mock(client, mocker):
    # CT-04: Mock OAuth
    # Mocking the OAuth authorize_access_token and userinfo
    mock_oauth = mocker.patch('app.controllers.auth_controller.oauth.google')
    mock_oauth.authorize_access_token.return_value = {'userinfo': {'email': 'oauth@test.com', 'name': 'OAuth User'}}
    
    response = client.get("/oauth/authorize", follow_redirects=True)
    assert response.status_code == 200
    with client.application.app_context():
        usuario = UsuarioModel.query.filter_by(email="oauth@test.com").first()
        assert usuario is not None
        assert usuario.role == "CLIENTE"
