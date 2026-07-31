from flask import Blueprint, jsonify
from app import db
from app.models import Multa

multas_bp = Blueprint("multas", __name__, url_prefix="/multas")


@multas_bp.route("", methods=["GET"])
def listar_multas():
    multas = Multa.query.filter_by(paga=False).all()
    return jsonify([
        {"id": m.id, "emprestimo_id": m.emprestimo_id, "valor": float(m.valor)}
        for m in multas
    ])


@multas_bp.route("/<int:multa_id>/pagar", methods=["POST"])
def pagar_multa(multa_id):
    multa = Multa.query.get_or_404(multa_id)
    multa.paga = True
    db.session.commit()
    return jsonify({"id": multa.id, "paga": True})
