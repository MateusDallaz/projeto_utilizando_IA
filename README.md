# Projeto utilizando IA

Sistema web com conexão direta ao MySQL. Módulo atual: **cadastro de clientes**.

- **Back end:** Python (Flask)
- **Front end:** HTML, CSS e JavaScript
- **Banco de dados:** MySQL

Os padrões de nomes de arquivos, tabelas e código estão em
[`docs/padroes_nomenclatura.md`](docs/padroes_nomenclatura.md).

## Estrutura (MVC)

O projeto é dividido em três camadas:

| Pasta | Camada | O que tem |
|-------|--------|-----------|
| `View/` | Front end | Telas HTML, CSS e JavaScript |
| `Control/` | Back end | Aplicação Flask, rotas e validação dos dados |
| `Model/` | Banco de dados | Conexão com o MySQL, SQL dos repositórios e scripts do banco |

```
projeto_utilizando_IA/
├── run.py                         # Ponto de entrada: python run.py
├── requirements.txt
├── .env.example                   # Modelo de configuração (sem senha real)
├── .gitignore                     # Bloqueia .env, senhas e certificados
│
├── View/                          # FRONT END
│   ├── templates/
│   │   ├── comum/base.html
│   │   └── clientes/clientes_cadastro.html
│   └── static/
│       ├── css/comum/             # base.css, formularios.css, tabelas.css
│       └── js/
│           ├── comum/             # api.js, aviso.js, etapas.js, formulario.js, mascaras.js, validadores.js
│           └── clientes/clientes_cadastro.js
│
├── Control/                       # BACK END
│   ├── __init__.py                # Cria a aplicação e registra os módulos
│   ├── config.py                  # Lê o .env
│   ├── comum/validadores.py       # Regras de validação reutilizáveis
│   └── clientes/
│       ├── clientes_rotas.py      # URLs da tela e da API
│       └── clientes_validacao.py  # Regras dos campos de clientes
│
├── Model/                         # BANCO DE DADOS
│   ├── conexao.py                 # Pool de conexões com o MySQL
│   ├── erros.py                   # Erros de banco (registro duplicado, não encontrado)
│   ├── clientes/clientes_repositorio.py   # Todo o SQL de clientes
│   ├── migracoes/001_criar_tabela_clientes.sql
│   └── dados_exemplo/001_clientes.sql
│
└── docs/padroes_nomenclatura.md
```

O caminho de uma requisição: **View** (tela) → **Control** (rota + validação) → **Model** (SQL) → MySQL.

## Como rodar

1. Crie o banco executando, em ordem, os arquivos de `Model/migracoes/`.
   Para ter dados de exemplo, execute também `Model/dados_exemplo/`.
   ```bash
   mysql -u root -p < Model/migracoes/001_criar_tabela_clientes.sql
   mysql -u root -p < Model/dados_exemplo/001_clientes.sql
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

## Regras de cadastro de clientes

| Campo    | Regra |
|----------|-------|
| Nome     | Nome e sobrenome, só letras, 3 a 100 caracteres. Salvo com iniciais maiúsculas. |
| E-mail   | Formato válido, sem espaços, único no banco. Salvo em minúsculas. |
| Telefone | DDD + número (10 ou 11 dígitos). Celular começa com 9. Salvo como `(47) 99999-1111`. |
| Cidade   | Só letras, sem sigla do estado. Salva com iniciais maiúsculas. |

Os campos são liberados **um por vez**, nessa ordem: o próximo só abre quando o atual está correto.

Os dados são validados no front end (para orientar o usuário) e novamente no back end
(para proteger o banco). A API aceita apenas um registro por requisição.

## Segurança

- **Nunca** envie o arquivo `.env`, senhas ou certificados digitais para o GitHub.
  O `.gitignore` já bloqueia esses arquivos.
- Antes de cada commit, confira com `git status` se nenhum arquivo sensível aparece na lista.
- Todas as consultas SQL usam parâmetros (`%s`), o que protege contra SQL Injection.
