"""
Rotas de autenticação.

  GET  /login   -> tela de login (e encerra qualquer sessão aberta)
  POST /login   -> confere usuário e senha
  GET  /sair    -> encerra a sessão e volta ao login
"""

from hmac import compare_digest

from flask import Blueprint, make_response, redirect, render_template, request, url_for

from Control.comum.seguranca import encerrar_sessao, liberar_acesso, sem_cache
from Model.usuarios import usuarios_repositorio as repositorio

autenticacao_bp = Blueprint("autenticacao", __name__)

TELA_INICIAL = "/clientes"
ERRO_LOGIN = "Usuário ou senha incorretos."


def _destino_seguro(caminho: str) -> str:
    """Só aceita caminhos internos do sistema (evita redirecionar para outro site)."""
    if caminho and caminho.startswith("/") and not caminho.startswith("//") and "\\" not in caminho:
        return caminho
    return TELA_INICIAL


def _tela(erro: str = "", usuario: str = "", status: int = 200):
    html = render_template(
        "autenticacao/autenticacao_login.html",
        erro=erro,
        usuario=usuario,
        proxima=_destino_seguro(request.values.get("proxima", "")),
    )
    return sem_cache(make_response(html, status))


@autenticacao_bp.get("/login")
def tela_login():
    encerrar_sessao()
    return _tela()


@autenticacao_bp.post("/login")
def entrar():
    usuario = request.form.get("usuario", "").strip()
    senha = request.form.get("senha", "")
    if not usuario or not senha:
        return _tela("Informe o usuário e a senha.", usuario, 400)

    registro = repositorio.buscar_por_usuario(usuario)
    # compare_digest leva o mesmo tempo para qualquer senha errada;
    # com usuário inexistente compara com um texto vazio para não dar pistas.
    senha_banco = registro["senha"] if registro else ""
    if not registro or not compare_digest(senha.encode(), senha_banco.encode()):
        return _tela(ERRO_LOGIN, usuario, 401)

    liberar_acesso(registro["usuario"])
    return redirect(_destino_seguro(request.form.get("proxima", "")))


@autenticacao_bp.get("/sair")
def sair():
    encerrar_sessao()
    return redirect(url_for("autenticacao.tela_login"))
