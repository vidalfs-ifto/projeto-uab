from app.database import db
from app.models.log_model import LogModel

def registrar_auditoria(autor_id, acao, afetado_id=None):
    log = LogModel(usuario_autor_id=autor_id, acao=acao, entidade_afetada_id=afetado_id)
    db.session.add(log)
    db.session.commit()
