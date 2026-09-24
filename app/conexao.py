"""Conexão direta com o MySQL, compartilhada por todos os módulos."""

from contextlib import contextmanager

import mysql.connector
from flask import current_app


@contextmanager
def obter_conexao():
    """
    Uso:
        with obter_conexao() as conexao:
            cursor = conexao.cursor(dictionary=True)
            ...
    A conexão é fechada automaticamente ao sair do bloco.
    """
    conexao = mysql.connector.connect(**current_app.config["DB_CONFIG"])
    try:
        yield conexao
    finally:
        conexao.close()
