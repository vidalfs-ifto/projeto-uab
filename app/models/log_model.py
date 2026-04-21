from app.database import db
from datetime import datetime

class LogModel(db.Model):
    __tablename__ = "logs"
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_autor_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    acao = db.Column(db.String(255), nullable=False)
    entidade_afetada_id = db.Column(db.Integer, nullable=True)
    data_hora = db.Column(db.DateTime, default=datetime.utcnow)
