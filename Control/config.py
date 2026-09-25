"""
Configurações da aplicação.

Os valores sensíveis vêm do arquivo .env, que NÃO vai para o GitHub.
"""

import os
import secrets

from dotenv import load_dotenv

load_dotenv()


class Config:
    DEBUG = os.getenv("FLASK_DEBUG", "false").lower() == "true"

    # Chave que assina o cookie de sessão. Sem SECRET_KEY no .env, é gerada
    # uma nova a cada início do servidor (reiniciar = todos voltam ao login).
    SECRET_KEY = os.getenv("SECRET_KEY") or secrets.token_hex(32)
    SESSION_COOKIE_HTTPONLY = True   # JavaScript não lê o cookie de sessão
    SESSION_COOKIE_SAMESITE = "Lax"  # outros sites não enviam o cookie em POSTs

    DB_CONFIG = {
        "host": os.getenv("DB_HOST", "localhost"),
        "port": int(os.getenv("DB_PORT", "3306")),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "database": os.getenv("DB_NAME", "projeto_utilizando_ia"),
        "charset": "utf8mb4",
        "collation": "utf8mb4_unicode_ci",
    }
