from flask import Blueprint, render_template, request, redirect, session, url_for
from app.models.usuario_model import UsuarioModel
from app.database import db

auth_controller = Blueprint('auth', __name__)

@auth_controller.route(
"/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        senha = request.form.get("senha")
        usuario = UsuarioModel.query.filter_by(email=email).first()
        if usuario and usuario.check_senha(senha):
            session["usuario_id"] = usuario.id
            session["usuario_role"] = usuario.role
            session["usuario_nome"] = usuario.nome
            return redirect("/dashboard")
        return redirect(url_for("auth.login", erro="credenciais"))
    return render_template("auth/login.html")

@auth_controller.route(
"/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")
        senha = request.form.get("senha")
        
        existente = UsuarioModel.query.filter_by(email=email).first()
        if existente:
            return redirect(url_for("auth.register", erro="email_cadastrado"))
            
        novo_cliente = UsuarioModel(nome=nome, email=email, role="CLIENTE")
        novo_cliente.set_senha(senha)
        db.session.add(novo_cliente)
        db.session.commit()
        return redirect(url_for("auth.login"))
    return render_template("auth/register.html")

@auth_controller.route(
"/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))

@auth_controller.route(
"/dashboard")
def dashboard():
    if "usuario_id" not in session:
        return redirect(url_for("auth.login"))
    return render_template("dashboard.html")

# Placeholder for OAuth
@auth_controller.route(
"/oauth/google")
def google_login():
    # Implementation would require authlib setup
    return "OAuth Google não configurado plenamente neste protótipo."
