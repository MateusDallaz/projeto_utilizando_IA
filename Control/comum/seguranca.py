"""
Controle de acesso às telas e à API.

Regra do projeto: toda vez que uma tela é aberta ou trocada, o sistema volta ao login.

  1. O login correto libera UMA abertura de tela (session["liberado"]).
  2. Ao abrir a tela, a liberação é consumida e é criado um token só para
     aquela tela. O JavaScript envia esse token à API no cabeçalho X-Token.
  3. Abrir qualquer tela sem liberação (recarregar, trocar de página, voltar,
     digitar o endereço) apaga a sessão e redireciona para o login.
"""

import secrets
from functools import wraps
from hmac import compare_digest

from flask import g, jsonify, make_response, redirect, request, session, url_for

CABECALHO_TOKEN = "X-Token"


def sem_cache(resposta):
    """Impede o navegador de guardar a tela (o botão Voltar não mostra dados antigos)."""
    resposta.headers["Cache-Control"] = "no-store"
    return resposta


def liberar_acesso(usuario: str) -> None:
    """Chamada após o login correto: libera a próxima abertura de tela."""
    session.clear()
    session["usuario"] = usuario
    session["liberado"] = True


def encerrar_sessao() -> None:
    session.clear()


def tela_protegida(funcao):
    """Decorador das rotas que devolvem telas (HTML)."""

    @wraps(funcao)
    def envolvida(*args, **kwargs):
        if not session.pop("liberado", False):
            encerrar_sessao()
            return redirect(url_for("autenticacao.tela_login", proxima=request.path))

        session["token"] = secrets.token_urlsafe(32)
        g.token = session["token"]
        g.usuario = session.get("usuario")
        return sem_cache(make_response(funcao(*args, **kwargs)))

    return envolvida


def api_protegida(funcao):
    """Decorador das rotas da API: exige o token da tela aberta."""

    @wraps(funcao)
    def envolvida(*args, **kwargs):
        token = session.get("token")
        enviado = request.headers.get(CABECALHO_TOKEN, "")
        if not token or not compare_digest(token, enviado):
            return jsonify({"erros": {"geral": "Sessão encerrada. Faça login novamente."}}), 401
        return funcao(*args, **kwargs)

    return envolvida
