import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "minha_chave_padrao")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(os.getcwd(), os.getenv("DATABASE_PATH", "app/db/atendimento.db"))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = os.getenv("DEBUG_MODE", "True").lower() == "true"
    PROPRIETARIO_EMAIL = os.getenv("PROPRIETARIO_EMAIL")
    PROPRIETARIO_PASSWORD = os.getenv("PROPRIETARIO_PASSWORD")
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
