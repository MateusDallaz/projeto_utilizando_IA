"""Criação da aplicação Flask e registro dos módulos."""

import logging
import mimetypes

import mysql.connector
from flask import Flask, jsonify, redirect, url_for

from app.config import Config

# No Windows, o registro às vezes entrega .js como text/plain,
# o que impede o navegador de carregar os módulos JavaScript.
mimetypes.add_type("application/javascript", ".js")

log = logging.getLogger(__name__)


def criar_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    logging.basicConfig(level=logging.INFO)

    # ---- Módulos (cada novo módulo é registrado aqui) ----
    from app.modulos.clientes.clientes_rotas import clientes_bp

    app.register_blueprint(clientes_bp)

    @app.get("/")
    def inicio():
        return redirect(url_for("clientes.tela_cadastro"))

    # ---- Erro de banco em qualquer rota: loga o detalhe, responde com mensagem segura ----
    @app.errorhandler(mysql.connector.Error)
    def erro_banco(exc):
        log.exception("Erro no banco de dados: %s", exc)
        return jsonify({"erros": {"geral": "Não foi possível acessar o banco de dados. Tente novamente."}}), 500

    return app
