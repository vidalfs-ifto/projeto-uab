from flask import Flask
from config import Config
from app.database import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    # Note: Blueprints will be imported here to avoid circular imports
    from app.controllers.auth_controller import auth_controller
    from app.controllers.usuario_controller import usuario_controller
    from app.controllers.ticket_controller import ticket_controller
    from app.controllers.relatorio_controller import relatorio_controller

    app.register_blueprint(auth_controller)
    app.register_blueprint(usuario_controller)
    app.register_blueprint(ticket_controller)
    app.register_blueprint(relatorio_controller)

    return app
