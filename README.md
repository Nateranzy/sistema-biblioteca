# Sistema de Biblioteca

Flask + PostgreSQL. Cadastro de livros, empréstimos, devoluções e multas.

## Como rodar

1. Crie um ambiente virtual e instale as dependências:
   ```
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Copie `.env.example` para `.env` e preencha com a senha real do PostgreSQL
   que você definiu na instalação:
   ```
   copy .env.example .env
   ```

3. Rode a aplicação (na primeira vez, ela já cria as tabelas no banco):
   ```
   python run.py
   ```

4. A API sobe em `http://localhost:5000`.

## Estrutura do projeto

```
biblioteca/
├── app/
│   ├── __init__.py          # application factory
│   ├── models.py             # Livro, Exemplar, Usuario, Emprestimo, Multa
│   ├── routes/                # rotas HTTP (Blueprints)
│   │   ├── livros.py
│   │   ├── emprestimos.py
│   │   └── multas.py
│   └── services/
│       └── emprestimo_service.py  # lógica de negócio + proteção de concorrência
├── config.py
├── run.py
├── requirements.txt
└── .env.example
```

## Endpoints principais

| Método | Rota | O que faz |
|---|---|---|
| POST | /livros | Cadastra livro (+ exemplares) |
| GET | /livros | Lista livros |
| GET | /livros/\<id\>/exemplares | Lista exemplares de um livro |
| POST | /emprestimos | Realiza empréstimo |
| POST | /emprestimos/\<id\>/devolucao | Registra devolução (gera multa se atrasado) |
| GET | /multas | Lista multas não pagas |
| POST | /multas/\<id\>/pagar | Marca multa como paga |

## Ponto de atenção: concorrência

Em `emprestimo_service.py`, o empréstimo usa um `UPDATE ... WHERE status = 'disponivel'`
atômico em vez de checar e depois gravar em dois passos separados. Isso evita que
dois usuários peguem o mesmo exemplar físico ao mesmo tempo.
