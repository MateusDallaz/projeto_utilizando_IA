"""
Configurações da aplicação.

Os valores sensíveis vêm do arquivo .env, que NÃO vai para o GitHub.
"""

import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    DEBUG = os.getenv("FLASK_DEBUG", "false").lower() == "true"

    DB_CONFIG = {
        "host": os.getenv("DB_HOST", "localhost"),
        "port": int(os.getenv("DB_PORT", "3306")),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "database": os.getenv("DB_NAME", "projeto_utilizando_ia"),
        "charset": "utf8mb4",
        "collation": "utf8mb4_unicode_ci",
    }
