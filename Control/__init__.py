"""
Control — back end (Flask).

Cria a aplicação, liga as telas e arquivos da pasta View,
configura a conexão da pasta Model e registra os módulos.
"""

import logging
import mimetypes
from pathlib import Path

import mysql.connector
from flask import Flask, jsonify, redirect, url_for

from Control.config import Config
from Model import conexao

# No Windows, o registro às vezes entrega .js como text/plain,
# o que impede o navegador de carregar os módulos JavaScript.
mimetypes.add_type("application/javascript", ".js")

PASTA_VIEW = Path(__file__).resolve().parent.parent / "View"

log = logging.getLogger(__name__)


def criar_app():
    app = Flask(
        __name__,
        template_folder=str(PASTA_VIEW / "templates"),
        static_folder=str(PASTA_VIEW / "static"),
    )
    app.config.from_object(Config)
    logging.basicConfig(level=logging.INFO)

    conexao.configurar(Config.DB_CONFIG)

    # ---- Módulos (cada novo módulo é registrado aqui) ----
    from Control.clientes.clientes_rotas import clientes_bp

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
