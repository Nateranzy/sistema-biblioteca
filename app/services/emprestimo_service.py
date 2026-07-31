from datetime import date
from sqlalchemy import text
from app import db
from app.models import Exemplar, Emprestimo, Multa
from flask import current_app


class ExemplarIndisponivelError(Exception):
    """Levantado quando o exemplar já foi emprestado por outra requisição."""
    pass


def realizar_emprestimo(exemplar_id: int, usuario_id: int) -> Emprestimo:
    """
    Ponto crítico do sistema: dois usuários podem tentar pegar o mesmo
    exemplar ao mesmo tempo. Por isso usamos UPDATE...WHERE atômico em vez
    de "SELECT depois UPDATE" (que teria uma janela de corrida).

    O PostgreSQL só afeta a linha se a condição WHERE ainda for verdadeira
    no exato momento da escrita — então só uma das duas requisições
    concorrentes consegue "ganhar" o exemplar.
    """
    resultado = db.session.execute(
        text(
            "UPDATE exemplares SET status = :emprestado "
            "WHERE id = :id AND status = :disponivel "
            "RETURNING id"
        ),
        {
            "id": exemplar_id,
            "emprestado": Exemplar.STATUS_EMPRESTADO,
            "disponivel": Exemplar.STATUS_DISPONIVEL,
        },
    )

    if resultado.rowcount == 0:
        db.session.rollback()
        raise ExemplarIndisponivelError(
            "Este exemplar não está disponível para empréstimo."
        )

    dias = current_app.config.get("DIAS_PARA_DEVOLUCAO", 14)
    emprestimo = Emprestimo(
        exemplar_id=exemplar_id,
        usuario_id=usuario_id,
        data_emprestimo=date.today(),
        data_prevista_devolucao=Emprestimo.calcular_data_prevista(dias),
    )
    db.session.add(emprestimo)
    db.session.commit()
    return emprestimo


def registrar_devolucao(emprestimo_id: int) -> Emprestimo:
    """
    Marca o empréstimo como devolvido, libera o exemplar, e gera multa
    automaticamente se a devolução estiver atrasada.
    """
    emprestimo = Emprestimo.query.get_or_404(emprestimo_id)
    emprestimo.data_devolucao = date.today()

    exemplar = Exemplar.query.get(emprestimo.exemplar_id)
    exemplar.status = Exemplar.STATUS_DISPONIVEL

    if emprestimo.esta_atrasado:
        dias_atraso = (emprestimo.data_devolucao - emprestimo.data_prevista_devolucao).days
        valor_por_dia = current_app.config.get("VALOR_MULTA_POR_DIA", 2.00)
        multa = Multa(
            emprestimo_id=emprestimo.id,
            valor=round(dias_atraso * valor_por_dia, 2),
            paga=False,
        )
        db.session.add(multa)

    db.session.commit()
    return emprestimo
