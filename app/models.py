from datetime import date, timedelta
from app import db


class Livro(db.Model):
    __tablename__ = "livros"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    autor = db.Column(db.String(150), nullable=False)
    isbn = db.Column(db.String(20), unique=True)
    categoria = db.Column(db.String(80))

    exemplares = db.relationship("Exemplar", backref="livro", lazy=True)

    def __repr__(self):
        return f"<Livro {self.titulo}>"


class Exemplar(db.Model):
    __tablename__ = "exemplares"

    # Status possíveis: disponivel, emprestado, perdido, manutencao
    STATUS_DISPONIVEL = "disponivel"
    STATUS_EMPRESTADO = "emprestado"

    id = db.Column(db.Integer, primary_key=True)
    livro_id = db.Column(db.Integer, db.ForeignKey("livros.id"), nullable=False)
    status = db.Column(db.String(20), nullable=False, default=STATUS_DISPONIVEL)

    emprestimos = db.relationship("Emprestimo", backref="exemplar", lazy=True)

    def __repr__(self):
        return f"<Exemplar {self.id} do livro {self.livro_id} ({self.status})>"


class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    ativo = db.Column(db.Boolean, default=True, nullable=False)

    emprestimos = db.relationship("Emprestimo", backref="usuario", lazy=True)

    def __repr__(self):
        return f"<Usuario {self.nome}>"


class Emprestimo(db.Model):
    __tablename__ = "emprestimos"

    id = db.Column(db.Integer, primary_key=True)
    exemplar_id = db.Column(db.Integer, db.ForeignKey("exemplares.id"), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    data_emprestimo = db.Column(db.Date, nullable=False, default=date.today)
    data_prevista_devolucao = db.Column(db.Date, nullable=False)
    data_devolucao = db.Column(db.Date, nullable=True)  # NULL enquanto não devolvido

    multa = db.relationship("Multa", backref="emprestimo", uselist=False)

    @staticmethod
    def calcular_data_prevista(dias=14):
        return date.today() + timedelta(days=dias)

    @property
    def esta_atrasado(self):
        if self.data_devolucao:
            return self.data_devolucao > self.data_prevista_devolucao
        return date.today() > self.data_prevista_devolucao

    def __repr__(self):
        return f"<Emprestimo {self.id} exemplar={self.exemplar_id}>"


class Multa(db.Model):
    __tablename__ = "multas"

    id = db.Column(db.Integer, primary_key=True)
    emprestimo_id = db.Column(db.Integer, db.ForeignKey("emprestimos.id"), nullable=False, unique=True)
    valor = db.Column(db.Numeric(10, 2), nullable=False)
    paga = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return f"<Multa {self.valor} paga={self.paga}>"
