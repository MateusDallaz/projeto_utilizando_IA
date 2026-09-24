"""
Conexão com o MySQL, compartilhada por todos os repositórios.

Usa um pool: as conexões são abertas uma vez e reaproveitadas,
em vez de abrir e fechar uma conexão nova a cada consulta.
"""

import threading
from contextlib import contextmanager

from mysql.connector import pooling

TAMANHO_POOL = 10

_config = {}
_pool = None
_trava = threading.Lock()


def configurar(db_config: dict) -> None:
    """Chamada uma vez na criação da aplicação, com os dados do .env."""
    global _config, _pool
    _config = dict(db_config)
    _pool = None


def _obter_pool():
    # O pool é criado no primeiro uso: assim o sistema abre mesmo se o banco
    # ainda estiver desligado, e o erro aparece só quando houver consulta.
    global _pool
    if _pool is None:
        with _trava:
            if _pool is None:
                _pool = pooling.MySQLConnectionPool(
                    pool_name="projeto", pool_size=TAMANHO_POOL, **_config
                )
    return _pool


@contextmanager
def obter_conexao():
    """
    Uso:
        with obter_conexao() as conexao:
            cursor = conexao.cursor(dictionary=True)
            ...
    Ao sair do bloco, a conexão volta para o pool.
    """
    conexao = _obter_pool().get_connection()
    try:
        yield conexao
    finally:
        conexao.close()
