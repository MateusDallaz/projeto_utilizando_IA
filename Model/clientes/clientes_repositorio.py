"""
Acesso ao banco de dados da tabela clientes.

Todo SQL do módulo fica aqui. Consultas sempre parametrizadas (%s),
o que protege contra SQL Injection.
"""

import mysql.connector

from Model.conexao import obter_conexao
from Model.erros import RegistroDuplicadoErro, RegistroNaoEncontradoErro

ERRO_DUPLICADO = 1062

SELECT_BASE = """
    SELECT id, nome, email, telefone, cidade,
           DATE_FORMAT(data_cadastro, '%d/%m/%Y %H:%i') AS data_cadastro
    FROM clientes
"""


def _buscar(cursor, cliente_id: int):
    cursor.execute(SELECT_BASE + " WHERE id = %s", (cliente_id,))
    return cursor.fetchone()


def _executar_gravacao(conexao, sql: str, parametros: tuple):
    """Executa INSERT/UPDATE e converte e-mail repetido em RegistroDuplicadoErro."""
    cursor = conexao.cursor(dictionary=True)
    try:
        cursor.execute(sql, parametros)
    except mysql.connector.IntegrityError as exc:
        if exc.errno == ERRO_DUPLICADO:
            raise RegistroDuplicadoErro("email") from exc
        raise
    conexao.commit()
    return cursor


def listar():
    with obter_conexao() as conexao:
        cursor = conexao.cursor(dictionary=True)
        cursor.execute(SELECT_BASE + " ORDER BY nome")
        return cursor.fetchall()


def inserir(dados: dict) -> dict:
    """Grava o cliente e devolve o registro como ficou no banco."""
    with obter_conexao() as conexao:
        cursor = _executar_gravacao(
            conexao,
            "INSERT INTO clientes (nome, email, telefone, cidade) VALUES (%s, %s, %s, %s)",
            (dados["nome"], dados["email"], dados["telefone"], dados["cidade"]),
        )
        return _buscar(cursor, cursor.lastrowid)


def atualizar(cliente_id: int, dados: dict) -> dict:
    """Altera o cliente e devolve o registro atualizado."""
    with obter_conexao() as conexao:
        cursor = conexao.cursor(dictionary=True)
        if not _buscar(cursor, cliente_id):
            raise RegistroNaoEncontradoErro()

        cursor = _executar_gravacao(
            conexao,
            "UPDATE clientes SET nome = %s, email = %s, telefone = %s, cidade = %s WHERE id = %s",
            (dados["nome"], dados["email"], dados["telefone"], dados["cidade"], cliente_id),
        )
        return _buscar(cursor, cliente_id)
