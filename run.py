"""Ponto de entrada da aplicação: python run.py"""

from app import criar_app

app = criar_app()

if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"])
