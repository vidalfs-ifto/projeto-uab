import pytest
from app.models.usuario_model import UsuarioModel
from app.database import db

def test_criar_admin_pelo_proprietario(client, init_database):
    # CT-05: Criar Admin
    # Primeiro login como Proprietário
    client.post("/login", data={
        "email": "admin@test.com",
        "senha": "password"
    })
    
    response = client.post("/proprietario/usuarios", data={
        "nome": "Novo Admin",
        "email": "novo_admin@test.com",
        "senha": "password123",
        "role": "ADMINISTRADOR"
    }, follow_redirects=True)
    
    assert response.status_code == 200
    with client.application.app_context():
        usuario = UsuarioModel.query.filter_by(email="novo_admin@test.com").first()
        assert usuario is not None
        assert usuario.role == "ADMINISTRADOR"

def test_bloqueio_hierarquico(client, init_database):
    # CT-07: Bloqueio Hierárquico - Admin não pode acessar rota de proprietário
    # Criar um Admin primeiro
    with client.application.app_context():
        a = UsuarioModel(nome="Admin Sub", email="sub@test.com", role="ADMINISTRADOR")
        a.set_senha("password")
        db.session.add(a)
        db.session.commit()
        
    client.post("/login", data={
        "email": "sub@test.com",
        "senha": "password"
    })
    
    response = client.get("/proprietario/usuarios")
    assert response.status_code == 403

def test_criar_atendente_pelo_admin(client, init_database):
    # CT-06: Criar Atendente
    with client.application.app_context():
        a = UsuarioModel(nome="Admin Sub", email="sub2@test.com", role="ADMINISTRADOR")
        a.set_senha("password")
        db.session.add(a)
        db.session.commit()
        
    client.post("/login", data={
        "email": "sub2@test.com",
        "senha": "password"
    })
    
    response = client.post("/admin/atendentes", data={
        "nome": "Atendente 1",
        "email": "atendente1@test.com",
        "senha": "password123"
    }, follow_redirects=True)
    
    assert response.status_code == 200
    with client.application.app_context():
        usuario = UsuarioModel.query.filter_by(email="atendente1@test.com").first()
        assert usuario is not None
        assert usuario.role == "ATENDENTE"
