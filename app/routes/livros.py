from flask import Blueprint, request, jsonify
from app import db
from app.models import Livro, Exemplar

livros_bp = Blueprint("livros", __name__, url_prefix="/livros")


@livros_bp.route("", methods=["GET"])
def listar_livros():
    livros = Livro.query.all()
    return jsonify([
        {"id": l.id, "titulo": l.titulo, "autor": l.autor, "isbn": l.isbn}
        for l in livros
    ])


@livros_bp.route("", methods=["POST"])
def cadastrar_livro():
    dados = request.get_json()
    livro = Livro(
        titulo=dados["titulo"],
        autor=dados["autor"],
        isbn=dados.get("isbn"),
        categoria=dados.get("categoria"),
    )
    db.session.add(livro)
    db.session.commit()

    # já cria N exemplares físicos, se informado
    quantidade = dados.get("quantidade_exemplares", 1)
    for _ in range(quantidade):
        db.session.add(Exemplar(livro_id=livro.id))
    db.session.commit()

    return jsonify({"id": livro.id, "titulo": livro.titulo}), 201


@livros_bp.route("/<int:livro_id>/exemplares", methods=["GET"])
def listar_exemplares(livro_id):
    exemplares = Exemplar.query.filter_by(livro_id=livro_id).all()
    return jsonify([{"id": e.id, "status": e.status} for e in exemplares])
