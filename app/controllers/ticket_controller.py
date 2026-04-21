from flask import Blueprint, render_template, request, redirect, session, url_for
from app.models.ticket_model import TicketModel
from app.database import db
from app.utils.auth_utils import requer_autenticacao, requer_roles

ticket_controller = Blueprint('ticket', __name__)

@ticket_controller.route
("/tickets")
@requer_autenticacao
def lista():
    if session["usuario_role"] == "CLIENTE":
        tickets = TicketModel.query.filter_by(cliente_id=session["usuario_id"]).all()
    else:
        # Administradores, Proprietários e Atendentes veem todos
        tickets = TicketModel.query.all()
    return render_template("tickets/lista.html", tickets=tickets)

@ticket_controller.route
("/tickets/novo", methods=["POST"])
@requer_autenticacao
@requer_roles(["CLIENTE"])
def novo():
    assunto = request.form.get("assunto")
    descricao = request.form.get("descricao")
    
    novo_ticket = TicketModel(
        cliente_id=session["usuario_id"],
        assunto=assunto,
        descricao=descricao
    )
    db.session.add(novo_ticket)
    db.session.commit()
    return redirect(url_for("ticket.lista"))

@ticket_controller.route
("/tickets/<int:ticket_id>/responder", methods=["POST"])
@requer_autenticacao
@requer_roles(["ATENDENTE", "ADMINISTRADOR", "PROPRIETARIO"])
def responder(ticket_id):
    ticket = TicketModel.query.get_or_404(ticket_id)
    novo_status = request.form.get("status")
    
    if novo_status:
        ticket.status = novo_status
        ticket.atendente_id = session["usuario_id"]
        db.session.commit()
        
    return redirect(url_for("ticket.lista"))
