"""Regras de validação dos campos de clientes."""

from Control.comum import validadores as v

REGRAS_CLIENTE = {
    "nome": v.validar_nome_pessoa,
    "email": v.validar_email,
    "telefone": v.validar_telefone,
    "cidade": v.validar_nome_lugar,
}


def validar_cliente(dados):
    return v.validar_registro(dados, REGRAS_CLIENTE)
