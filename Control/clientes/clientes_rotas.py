"""
Rotas do módulo clientes.

  GET  /clientes            -> tela de cadastro
  GET  /api/clientes        -> lista os clientes
  POST /api/clientes        -> cadastra UM cliente
  PUT  /api/clientes/<id>   -> altera UM cliente

Todas exigem login (ver Control/comum/seguranca.py).
"""

from flask import Blueprint, jsonify, render_template, request

from Control.clientes.clientes_validacao import validar_cliente
from Control.comum.seguranca import api_protegida, tela_protegida
from Model.clientes import clientes_repositorio as repositorio
from Model.erros import RegistroDuplicadoErro, RegistroNaoEncontradoErro

clientes_bp = Blueprint("clientes", __name__)


@clientes_bp.get("/clientes")
@tela_protegida
def tela_cadastro():
    return render_template("clientes/clientes_cadastro.html")


@clientes_bp.get("/api/clientes")
@api_protegida
def listar_clientes():
    return jsonify(repositorio.listar())


@clientes_bp.post("/api/clientes")
@api_protegida
def cadastrar_cliente():
    dados, erros = validar_cliente(request.get_json(silent=True))
    if erros:
        return jsonify({"erros": erros}), 400

    try:
        cliente = repositorio.inserir(dados)
    except RegistroDuplicadoErro:
        return jsonify({"erros": {"email": "Já existe um cliente com este e-mail."}}), 409

    return jsonify(cliente), 201


@clientes_bp.put("/api/clientes/<int:cliente_id>")
@api_protegida
def alterar_cliente(cliente_id):
    dados, erros = validar_cliente(request.get_json(silent=True))
    if erros:
        return jsonify({"erros": erros}), 400

    try:
        cliente = repositorio.atualizar(cliente_id, dados)
    except RegistroNaoEncontradoErro:
        return jsonify({"erros": {"geral": "Cliente não encontrado. Atualize a lista."}}), 404
    except RegistroDuplicadoErro:
        return jsonify({"erros": {"email": "Este e-mail já pertence a outro cliente."}}), 409

    return jsonify(cliente)
