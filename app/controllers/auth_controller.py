from flask import Blueprint, render_template, request, redirect, session, url_for, current_app
from app.models.usuario_model import UsuarioModel
from app.database import db
from authlib.integrations.flask_client import OAuth

auth_controller = Blueprint('auth', __name__)
oauth = OAuth()

@auth_controller.record_once
def on_load(state):
    oauth.init_app(state.app)
    oauth.register(
        name='google',
        client_id=state.app.config.get('GOOGLE_CLIENT_ID'),
        client_secret=state.app.config.get('GOOGLE_CLIENT_SECRET'),
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={'scope': 'openid email profile'}
    )

@auth_controller.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        senha = request.form.get("senha")
        usuario = UsuarioModel.query.filter_by(email=email).first()
        if usuario and usuario.check_senha(senha):
            session["usuario_id"] = usuario.id
            session["usuario_role"] = usuario.role
            return redirect("/dashboard")
        return redirect("/login?erro=credenciais")
    return render_template("auth/login.html")

@auth_controller.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")
        senha = request.form.get("senha")
        
        novo_cliente = UsuarioModel(nome=nome, email=email, role="CLIENTE")
        novo_cliente.set_senha(senha)
        db.session.add(novo_cliente)
        db.session.commit()
        return redirect("/login")
    return render_template("auth/register.html")

@auth_controller.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@auth_controller.route("/oauth/google")
def google_login():
    redirect_uri = url_for('auth.google_authorize', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@auth_controller.route("/oauth/authorize")
def google_authorize():
    token = oauth.google.authorize_access_token()
    user_info = token.get('userinfo')
    if user_info:
        email = user_info['email']
        usuario = UsuarioModel.query.filter_by(email=email).first()
        if not usuario:
            usuario = UsuarioModel(nome=user_info.get('name', email), email=email, role="CLIENTE")
            # For OAuth users, we might not have a password, or set a random one
            usuario.set_senha("OAUTH_USER_NO_PASSWORD") 
            db.session.add(usuario)
            db.session.commit()
        
        session["usuario_id"] = usuario.id
        session["usuario_role"] = usuario.role
        return redirect("/dashboard")
    return redirect("/login?erro=oauth")

@auth_controller.route("/dashboard")
def dashboard():
    if "usuario_id" not in session:
        return redirect("/login")
    return render_template("dashboard.html")
