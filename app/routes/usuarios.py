from flask import Blueprint, request, jsonify, render_template
from app import db
from app.models import Usuario

usuarios_bp = Blueprint("usuarios", __name__)


@usuarios_bp.route("/cadastro", methods=["GET"])
def pagina_cadastro():
    return render_template("cadastro.html")


@usuarios_bp.route("/usuarios", methods=["POST"])
def cadastrar_usuario():
    dados = request.get_json()
    nome = dados.get("nome", "").strip()
    email = dados.get("email", "").strip()

    if not nome or not email:
        return jsonify({"erro": "Nome e email são obrigatórios."}), 400

    if Usuario.query.filter_by(email=email).first():
        return jsonify({"erro": "Este email já está cadastrado."}), 409

    usuario = Usuario(nome=nome, email=email, ativo=True)
    db.session.add(usuario)
    db.session.commit()

    return jsonify({"id": usuario.id, "nome": usuario.nome}), 201

@usuarios_bp.route("/usuarios", methods=["GET"])
def listar_usuarios():
    usuarios = Usuario.query.all()
    return jsonify([
        {"id": u.id, "nome": u.nome, "email": u.email, "ativo": u.ativo}
        for u in usuarios
    ])