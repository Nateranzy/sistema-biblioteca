from flask import Blueprint, request, jsonify
from app.services.emprestimo_service import (
    realizar_emprestimo,
    registrar_devolucao,
    ExemplarIndisponivelError,
)

emprestimos_bp = Blueprint("emprestimos", __name__, url_prefix="/emprestimos")


@emprestimos_bp.route("", methods=["POST"])
def criar_emprestimo():
    dados = request.get_json()
    try:
        emprestimo = realizar_emprestimo(
            exemplar_id=dados["exemplar_id"],
            usuario_id=dados["usuario_id"],
        )
    except ExemplarIndisponivelError as erro:
        # 409 Conflict: alguém pegou o exemplar primeiro
        return jsonify({"erro": str(erro)}), 409

    return jsonify({
        "id": emprestimo.id,
        "data_prevista_devolucao": emprestimo.data_prevista_devolucao.isoformat(),
    }), 201


@emprestimos_bp.route("/<int:emprestimo_id>/devolucao", methods=["POST"])
def devolver(emprestimo_id):
    emprestimo = registrar_devolucao(emprestimo_id)
    resposta = {"id": emprestimo.id, "devolvido_em": emprestimo.data_devolucao.isoformat()}
    if emprestimo.multa:
        resposta["multa_gerada"] = float(emprestimo.multa.valor)
    return jsonify(resposta)
