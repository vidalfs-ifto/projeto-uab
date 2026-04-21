from app import create_app
from app.database import db
from app.models.usuario_model import UsuarioModel
from config import Config
import os

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db_path = os.path.dirname(Config.SQLALCHEMY_DATABASE_URI.replace("sqlite:///", ""))
        if not os.path.exists(db_path):
            os.makedirs(db_path)
            
        db.create_all()
        
        proprietario = UsuarioModel.query.filter_by(email=Config.PROPRIETARIO_EMAIL).first()
        if not proprietario:
            novo_proprietario = UsuarioModel(
                nome="Proprietário Inicial",
                email=Config.PROPRIETARIO_EMAIL, 
                role="PROPRIETARIO"
            )
            novo_proprietario.set_senha(Config.PROPRIETARIO_PASSWORD)
            db.session.add(novo_proprietario)
            db.session.commit()
            print(f"Proprietário inicial criado: {Config.PROPRIETARIO_EMAIL}")
        
    app.run(host="0.0.0.0", port=5000)
