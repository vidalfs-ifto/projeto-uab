import pytest
from app.models.usuario_model import UsuarioModel
from app.models.ticket_model import TicketModel
from app.database import db

@pytest.fixture
def admin_user(app):
    with app.app_context():
        admin = UsuarioModel(nome="Admin 1", email="admin1@test.com", role="ADMINISTRADOR")
        admin.set_senha("password")
        db.session.add(admin)
        db.session.commit()
        return admin

def test_filtro_relatorio_geral(client, admin_user):
    # CT-11: Filtro Relatório
    client.post("/login", data={
        "email": "admin1@test.com",
        "senha": "password"
    })
    
    response = client.get("/admin/relatorios?tipo=geral")
    assert response.status_code == 200
    # Add more assertions based on expected content in template if known
    # Since templates are basic, we just check status code for now

def test_filtro_relatorio_por_admin(client, admin_user):
    client.post("/login", data={
        "email": "admin1@test.com",
        "senha": "password"
    })
    
    response = client.get("/admin/relatorios?tipo=por_admin")
    assert response.status_code == 200

def test_acesso_negado_relatorio_cliente(client, app):
    with app.app_context():
        cliente = UsuarioModel(nome="Cliente", email="cliente@test.com", role="CLIENTE")
        cliente.set_senha("password")
        db.session.add(cliente)
        db.session.commit()
        
    client.post("/login", data={
        "email": "cliente@test.com",
        "senha": "password"
    })
    
    response = client.get("/admin/relatorios?tipo=geral")
    assert response.status_code == 403
