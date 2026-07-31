import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Nunca coloque a senha do banco direto no código.
    # Ela vem do arquivo .env (veja .env.example)
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "postgresql://postgres:SUA_SENHA@localhost:5432/biblioteca_db",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY", "troque-isso-em-producao")

    # Regra de negócio: prazo padrão de devolução
    DIAS_PARA_DEVOLUCAO = 14
    VALOR_MULTA_POR_DIA = 2.00
