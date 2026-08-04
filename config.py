import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Nunca coloque a senha do banco direto no código.
    # Ela vem do arquivo .env (veja .env.example)
    _raw_db_url = os.environ.get(
        "DATABASE_URL",
        "postgresql://postgres:SUA_SENHA@localhost:5432/biblioteca_db",
    )
    # Garante que o SQLAlchemy use o driver psycopg (v3), não o psycopg2
    if _raw_db_url.startswith("postgresql://"):
        _raw_db_url = _raw_db_url.replace("postgresql://", "postgresql+psycopg://", 1)

    SQLALCHEMY_DATABASE_URI = _raw_db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY", "troque-isso-em-producao")

    # Regra de negócio: prazo padrão de devolução
    DIAS_PARA_DEVOLUCAO = 14
    VALOR_MULTA_POR_DIA = 2.00