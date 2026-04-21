from flask import Blueprint, render_template, request, redirect, session, url_for, abort
from app.models.usuario_model import UsuarioModel
from app.database import db
from app.utils.auth_utils import requer_autenticacao, requer_roles
from app.utils.log_utils import registrar_auditoria

usuario_controller = Blueprint('usuario', __name__)

@usuario_controller.route
("/proprietario/usuarios", methods=["GET", "POST"])
@requer_autenticacao
@requer_roles(["PROPRIETARIO"])
def gestao_proprietario():
    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")
        senha = request.form.get("senha")
        role_alvo = request.form.get("role") # ADMINISTRADOR ou PROPRIETARIO
        
        if role_alvo not in ["ADMINISTRADOR", "PROPRIETARIO"]:
             abort(400) # Bad Request
             
        novo_usuario = UsuarioModel(nome=nome, email=email, role=role_alvo, criado_por_id=session["usuario_id"])
        novo_usuario.set_senha(senha)
        db.session.add(novo_usuario)
        db.session.commit()
        
        registrar_auditoria(session["usuario_id"], "CRIAR_" + role_alvo, novo_usuario.id)
        return redirect(url_for("usuario.gestao_proprietario"))
        
    usuarios = UsuarioModel.query.filter(UsuarioModel.role.in_(["PROPRIETARIO", "ADMINISTRADOR"])).all()
    return render_template("admin/gestao_proprietario.html", usuarios=usuarios)

@usuario_controller.route
("/admin/atendentes", methods=["GET", "POST"])
@requer_autenticacao
@requer_roles(["ADMINISTRADOR", "PROPRIETARIO"])
def gestao_admin():
    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")
        senha = request.form.get("senha")
        
        novo_atendente = UsuarioModel(nome=nome, email=email, role="ATENDENTE", criado_por_id=session["usuario_id"])
        novo_atendente.set_senha(senha)
        db.session.add(novo_atendente)
        db.session.commit()
        
        registrar_auditoria(session["usuario_id"], "CRIAR_ATENDENTE", novo_atendente.id)
        return redirect(url_for("usuario.gestao_admin"))
        
    atendentes = UsuarioModel.query.filter_by(role="ATENDENTE").all()
    return render_template("admin/gestao_admin.html", atendentes=atendentes)
