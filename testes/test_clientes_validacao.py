"""
Testes da validação de clientes.
Rodar com:  python -m pytest
"""

from app.modulos.clientes.clientes_validacao import validar_cliente

VALIDO = {
    "nome": "  MARIA   DA silva ",
    "email": " Maria@Email.COM ",
    "telefone": "47999991111",
    "cidade": "rio DO sul",
}


def test_padroniza_dados_validos():
    dados, erros = validar_cliente(VALIDO)
    assert erros == {}
    assert dados == {
        "nome": "Maria da Silva",
        "email": "maria@email.com",
        "telefone": "(47) 99999-1111",
        "cidade": "Rio do Sul",
    }


def test_telefone_fixo_formatado():
    dados, _ = validar_cliente({**VALIDO, "telefone": "4733331111"})
    assert dados["telefone"] == "(47) 3333-1111"


def test_exige_nome_e_sobrenome():
    _, erros = validar_cliente({**VALIDO, "nome": "João"})
    assert "nome" in erros


def test_recusa_email_invalido():
    _, erros = validar_cliente({**VALIDO, "email": "a..b@c.com"})
    assert "email" in erros


def test_recusa_celular_sem_nove():
    _, erros = validar_cliente({**VALIDO, "telefone": "47888881111"})
    assert "telefone" in erros


def test_recusa_simbolos_no_nome():
    _, erros = validar_cliente({**VALIDO, "nome": "x'; DROP TABLE clientes;--"})
    assert "nome" in erros


def test_aceita_apenas_um_registro_por_vez():
    _, erros = validar_cliente([VALIDO, VALIDO])
    assert "geral" in erros
