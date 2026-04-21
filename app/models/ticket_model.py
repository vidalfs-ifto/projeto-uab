from app.database import db
from datetime import datetime

class TicketModel(db.Model):
    __tablename__ = "tickets"
    
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    atendente_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=True)
    assunto = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    status = db.Column(db.Enum("ABERTO", "EM_ANDAMENTO", "RESOLVIDO", "FECHADO"), default="ABERTO")
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
