import pytest
from app.models.usuario_model import UsuarioModel
from app.models.ticket_model import TicketModel
from app.database import db

@pytest.fixture
def users(app):
    with app.app_context():
        cliente = UsuarioModel(nome="Cliente 1", email="cliente1@test.com", role="CLIENTE")
        cliente.set_senha("password")
        atendente = UsuarioModel(nome="Atendente 1", email="atendente1@test.com", role="ATENDENTE")
        atendente.set_senha("password")
        db.session.add(cliente)
        db.session.add(atendente)
        db.session.commit()
        return {
            "cliente": cliente,
            "atendente": atendente
        }

def test_abertura_ticket(client, users):
    # CT-08: Abertura Ticket
    client.post("/login", data={
        "email": "cliente1@test.com",
        "senha": "password"
    })
    
    response = client.post("/tickets/novo", data={
        "assunto": "Problema Técnico",
        "descricao": "Meu computador não liga"
    }, follow_redirects=True)
    
    assert response.status_code == 200
    with client.application.app_context():
        ticket = TicketModel.query.filter_by(assunto="Problema Técnico").first()
        assert ticket is not None
        assert ticket.status == "ABERTO"
        assert ticket.cliente_id is not None

def test_resposta_ticket(client, users):
    # CT-09: Resposta Ticket
    with client.application.app_context():
        # Get the ID of the client user from the session-detached object
        cliente = UsuarioModel.query.filter_by(email="cliente1@test.com").first()
        t = TicketModel(cliente_id=cliente.id, assunto="Assunto", descricao="Desc")
        db.session.add(t)
        db.session.commit()
        ticket_id = t.id
        
    client.post("/login", data={
        "email": "atendente1@test.com",
        "senha": "password"
    })
    
    response = client.post(f"/tickets/{ticket_id}/responder", data={
        "status": "EM_ANDAMENTO"
    }, follow_redirects=True)
    
    assert response.status_code == 200
    with client.application.app_context():
        ticket = TicketModel.query.get(ticket_id)
        assert ticket.status == "EM_ANDAMENTO"
        assert ticket.atendente_id is not None

def test_visibilidade_tickets(client, users):
    # CT-10: Visibilidade
    with client.application.app_context():
        c1 = UsuarioModel.query.filter_by(email="cliente1@test.com").first()
        c2 = UsuarioModel(nome="Cliente 2", email="cliente2@test.com", role="CLIENTE")
        c2.set_senha("password")
        db.session.add(c2)
        db.session.commit()
        
        t1 = TicketModel(cliente_id=c1.id, assunto="Ticket Cliente 1", descricao="...")
        t2 = TicketModel(cliente_id=c2.id, assunto="Ticket Cliente 2", descricao="...")
        db.session.add(t1)
        db.session.add(t2)
        db.session.commit()
    
    # Login como Cliente 1 - deve ver apenas seu ticket
    client.post("/login", data={"email": "cliente1@test.com", "senha": "password"})
    response = client.get("/tickets")
    assert b"Ticket Cliente 1" in response.data
    assert b"Ticket Cliente 2" not in response.data
    
    client.get("/logout")
    
    # Login como Atendente - deve ver todos os tickets
    client.post("/login", data={"email": "atendente1@test.com", "senha": "password"})
    response = client.get("/tickets")
    assert b"Ticket Cliente 1" in response.data
    assert b"Ticket Cliente 2" in response.data
