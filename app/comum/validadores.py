"""
Validadores reutilizáveis por qualquer módulo.

Cada função recebe o texto digitado e devolve (valor_tratado, erro):
  - erro None -> valor_tratado pronto para gravar
  - erro str  -> mensagem para o usuário
"""

import re

LETRAS = "A-Za-zÀ-ÖØ-öø-ÿ"

# Palavras (com acentos), separadas por espaço, hífen ou apóstrofo
PALAVRAS_RE = re.compile(rf"^[{LETRAS}]+(?:[ '\-][{LETRAS}]+)*$")
EMAIL_RE = re.compile(r"^[a-z0-9._%+\-]+@[a-z0-9\-]+(\.[a-z0-9\-]+)*\.[a-z]{2,}$")

# Mantidas em minúsculo no meio de nomes: "Maria da Silva", "Rio do Sul"
PREPOSICOES = {"da", "de", "do", "das", "dos", "e"}


# ------------------------------------------------------------
# Auxiliares de formatação
# ------------------------------------------------------------
def limpar_espacos(valor: str) -> str:
    """Remove espaços no início/fim e espaços duplicados no meio."""
    return re.sub(r"\s+", " ", valor.strip())


def capitalizar(texto: str) -> str:
    """'MARIA DA SILVA' -> 'Maria da Silva'; "d'ávila" -> "D'Ávila"."""
    palavras = texto.lower().split(" ")
    resultado = []
    for i, palavra in enumerate(palavras):
        if i > 0 and palavra in PREPOSICOES:
            resultado.append(palavra)
        else:
            resultado.append(re.sub(r"(^|[-'])(.)", lambda m: m.group(1) + m.group(2).upper(), palavra))
    return " ".join(resultado)


# ------------------------------------------------------------
# Validadores de campo
# ------------------------------------------------------------
def validar_nome_pessoa(valor: str):
    nome = limpar_espacos(valor)
    if not nome:
        return None, "Informe o nome completo."
    if len(nome) < 3 or len(nome) > 100:
        return None, "O nome deve ter entre 3 e 100 caracteres."
    if not PALAVRAS_RE.match(nome):
        return None, "Use apenas letras no nome, sem números ou símbolos."
    if len(nome.split(" ")) < 2:
        return None, "Informe nome e sobrenome."
    return capitalizar(nome), None


def validar_email(valor: str):
    email = valor.strip().lower()
    if not email:
        return None, "Informe o e-mail."
    if len(email) > 150:
        return None, "O e-mail deve ter no máximo 150 caracteres."
    if " " in email or ".." in email or not EMAIL_RE.match(email):
        return None, "E-mail inválido. Exemplo correto: nome@empresa.com.br"
    return email, None


def validar_telefone(valor: str):
    digitos = re.sub(r"\D", "", valor)
    if not digitos:
        return None, "Informe o telefone."
    if len(digitos) not in (10, 11):
        return None, "O telefone deve ter DDD + número (10 ou 11 dígitos)."
    if digitos[0] == "0" or digitos[1] == "0":
        return None, "DDD inválido. Use dois dígitos, sem o zero: 47, 11, 48..."
    if len(digitos) == 11 and digitos[2] != "9":
        return None, "Celular com 11 dígitos deve começar com 9 após o DDD."

    # Sempre no mesmo formato: (47) 99999-1111 ou (47) 3333-1111
    ddd, numero = digitos[:2], digitos[2:]
    corte = 5 if len(numero) == 9 else 4
    return f"({ddd}) {numero[:corte]}-{numero[corte:]}", None


def validar_nome_lugar(valor: str):
    """Cidades, bairros, estados por extenso..."""
    lugar = limpar_espacos(valor)
    if not lugar:
        return None, "Informe a cidade."
    if len(lugar) < 2 or len(lugar) > 100:
        return None, "A cidade deve ter entre 2 e 100 caracteres."
    if not PALAVRAS_RE.match(lugar):
        return None, "Use apenas letras na cidade, sem a sigla do estado."
    return capitalizar(lugar), None


# ------------------------------------------------------------
# Validação de um registro completo
# ------------------------------------------------------------
def validar_registro(dados, regras: dict):
    """
    dados:  JSON recebido do front end
    regras: {"campo": funcao_validadora, ...}

    Retorna (dados_limpos, erros). Aceita apenas UM registro por vez:
    listas ou qualquer coisa que não seja um objeto simples são recusadas.
    """
    if not isinstance(dados, dict):
        return None, {"geral": "Envie apenas um registro por vez."}

    limpos, erros = {}, {}
    for campo, validador in regras.items():
        valor = dados.get(campo, "")
        if not isinstance(valor, str):
            erros[campo] = "Valor inválido."
            continue
        resultado, erro = validador(valor)
        if erro:
            erros[campo] = erro
        else:
            limpos[campo] = resultado

    return (None, erros) if erros else (limpos, {})
