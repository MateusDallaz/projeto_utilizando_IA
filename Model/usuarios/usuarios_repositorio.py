"""Acesso ao banco de dados da tabela Usuario (login do sistema)."""

from Model.conexao import obter_conexao


def buscar_por_usuario(usuario: str):
    """Devolve {id, usuario, senha} ou None se o usuário não existir."""
    with obter_conexao() as conexao:
        cursor = conexao.cursor(dictionary=True)
        cursor.execute("SELECT id, usuario, senha FROM Usuario WHERE usuario = %s LIMIT 1", (usuario,))
        return cursor.fetchone()
