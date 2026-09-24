# Projeto utilizando IA

Sistema web com conexão direta ao MySQL. Módulo atual: **cadastro de clientes**.

- **Back end:** Python (Flask)
- **Front end:** HTML, CSS e JavaScript
- **Banco de dados:** MySQL

Os padrões de nomes de arquivos, tabelas e código estão em
[`docs/padroes_nomenclatura.md`](docs/padroes_nomenclatura.md).

## Estrutura

```
projeto_utilizando_IA/
├── run.py                         # Ponto de entrada: python run.py
├── requirements.txt
├── pytest.ini
├── .env.example                   # Modelo de configuração (sem senha real)
├── .gitignore                     # Bloqueia .env, senhas e certificados
│
├── app/
│   ├── __init__.py                # Cria a aplicação e registra os módulos
│   ├── config.py                  # Lê o .env
│   ├── conexao.py                 # Conexão com o MySQL
│   ├── comum/                     # Código compartilhado entre módulos
│   │   ├── erros.py
│   │   └── validadores.py
│   ├── modulos/
│   │   └── clientes/
│   │       ├── clientes_rotas.py
│   │       ├── clientes_repositorio.py
│   │       └── clientes_validacao.py
│   ├── templates/
│   │   ├── comum/base.html
│   │   └── clientes/clientes_cadastro.html
│   └── static/
│       ├── css/comum/             # base.css, formularios.css, tabelas.css
│       └── js/
│           ├── comum/             # api.js, aviso.js, formulario.js, mascaras.js, validadores.js
│           └── clientes/clientes_cadastro.js
│
├── banco_dados/
│   ├── migracoes/001_criar_tabela_clientes.sql
│   └── dados_exemplo/001_clientes.sql
│
├── docs/padroes_nomenclatura.md
└── testes/test_clientes_validacao.py
```

## Como rodar

1. Crie o banco executando, em ordem, os arquivos de `banco_dados/migracoes/`.
   Para ter dados de teste, execute também `banco_dados/dados_exemplo/`.
   ```bash
   mysql -u root -p < banco_dados/migracoes/001_criar_tabela_clientes.sql
   mysql -u root -p < banco_dados/dados_exemplo/001_clientes.sql
   ```
2. Crie e ative um ambiente virtual:
   ```bash
   python -m venv venv
   venv\Scripts\activate        # Windows
   source venv/bin/activate     # Linux/Mac
   ```
3. Instale as dependências: `pip install -r requirements.txt`
4. Copie `.env.example` para `.env` e preencha usuário e senha do MySQL.
5. Inicie: `python run.py`
6. Acesse http://127.0.0.1:5000

Para rodar os testes: `python -m pytest`

## Regras de cadastro de clientes

| Campo    | Regra |
|----------|-------|
| Nome     | Nome e sobrenome, só letras, 3 a 100 caracteres. Salvo com iniciais maiúsculas. |
| E-mail   | Formato válido, sem espaços, único no banco. Salvo em minúsculas. |
| Telefone | DDD + número (10 ou 11 dígitos). Celular começa com 9. Salvo como `(47) 99999-1111`. |
| Cidade   | Só letras, sem sigla do estado. Salva com iniciais maiúsculas. |

Os dados são validados no front end (para orientar o usuário) e novamente no back end
(para proteger o banco). A API aceita apenas um registro por requisição.

## Segurança

- **Nunca** envie o arquivo `.env`, senhas ou certificados digitais para o GitHub.
  O `.gitignore` já bloqueia esses arquivos.
- Antes de cada commit, confira com `git status` se nenhum arquivo sensível aparece na lista.
- Todas as consultas SQL usam parâmetros (`%s`), o que protege contra SQL Injection.
