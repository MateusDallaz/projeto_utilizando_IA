"""
Acesso ao banco de dados da tabela clientes.

Todo SQL do módulo fica aqui. Consultas sempre parametrizadas (%s),
o que protege contra SQL Injection.
"""

import mysql.connector

from app.comum.erros import RegistroDuplicadoErro, RegistroNaoEncontradoErro
from app.conexao import obter_conexao

ERRO_DUPLICADO = 1062

SELECT_BASE = """
    SELECT id, nome, email, telefone, cidade,
           DATE_FORMAT(data_cadastro, '%d/%m/%Y %H:%i') AS data_cadastro
    FROM clientes
"""


def listar():
    with obter_conexao() as conexao:
        cursor = conexao.cursor(dictionary=True)
        cursor.execute(SELECT_BASE + " ORDER BY nome")
        return cursor.fetchall()


def buscar_por_id(cliente_id: int):
    with obter_conexao() as conexao:
        cursor = conexao.cursor(dictionary=True)
        cursor.execute(SELECT_BASE + " WHERE id = %s", (cliente_id,))
        return cursor.fetchone()


def inserir(dados: dict) -> int:
    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        try:
            cursor.execute(
                "INSERT INTO clientes (nome, email, telefone, cidade) VALUES (%s, %s, %s, %s)",
                (dados["nome"], dados["email"], dados["telefone"], dados["cidade"]),
            )
        except mysql.connector.IntegrityError as exc:
            if exc.errno == ERRO_DUPLICADO:
                raise RegistroDuplicadoErro("email") from exc
            raise
        conexao.commit()
        return cursor.lastrowid


def atualizar(cliente_id: int, dados: dict) -> None:
    if not buscar_por_id(cliente_id):
        raise RegistroNaoEncontradoErro()

    with obter_conexao() as conexao:
        cursor = conexao.cursor()
        try:
            cursor.execute(
                "UPDATE clientes SET nome = %s, email = %s, telefone = %s, cidade = %s WHERE id = %s",
                (dados["nome"], dados["email"], dados["telefone"], dados["cidade"], cliente_id),
            )
        except mysql.connector.IntegrityError as exc:
            if exc.errno == ERRO_DUPLICADO:
                raise RegistroDuplicadoErro("email") from exc
            raise
        conexao.commit()
