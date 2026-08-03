from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)

    from app.routes.livros import livros_bp
    from app.routes.emprestimos import emprestimos_bp
    from app.routes.multas import multas_bp
    from app.routes.usuarios import usuarios_bp

    app.register_blueprint(livros_bp)
    app.register_blueprint(emprestimos_bp)
    app.register_blueprint(multas_bp)
    app.register_blueprint(usuarios_bp)

    with app.app_context():
        db.create_all()

    return app