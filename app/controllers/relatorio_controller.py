from flask import Blueprint, render_template, request, session
from app.models.ticket_model import TicketModel
from app.models.usuario_model import UsuarioModel
from app.utils.auth_utils import requer_autenticacao, requer_roles
from app.database import db
from sqlalchemy import func

relatorio_controller = Blueprint('relatorio', __name__)

@relatorio_controller.route("/admin/relatorios")
@requer_autenticacao
@requer_roles(["ADMINISTRADOR"])
def relatorios():
    filtro = request.args.get("tipo")
    dados_relatorio = None
    
    if filtro == "geral":
        dados_relatorio = {
            'total': TicketModel.query.count(),
            'por_status': db.session.query(TicketModel.status, func.count(TicketModel.id)).group_by(TicketModel.status).all()
        }
    elif filtro == "por_atendente":
        atendente_id = request.args.get("atendente_id")
        if atendente_id:
            atendente = UsuarioModel.query.get(atendente_id)
            dados_relatorio = {
                'total': TicketModel.query.filter_by(atendente_id=atendente_id).count(),
                'atendente': atendente.nome if atendente else "Desconhecido"
            }
    elif filtro == "por_admin":
        lista_meus_atendentes = UsuarioModel.query.filter_by(criado_por_id=session["usuario_id"]).all()
        atendente_ids = [a.id for a in lista_meus_atendentes]
        dados_relatorio = {
            'total': TicketModel.query.filter(TicketModel.atendente_id.in_(atendente_ids)).count() if atendente_ids else 0,
            'atendentes_count': len(atendente_ids)
        }

    return render_template("admin/relatorios.html", relatorio=dados_relatorio)
