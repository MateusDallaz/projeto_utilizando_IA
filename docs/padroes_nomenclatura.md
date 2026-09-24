# Padrões de nomenclatura

Este documento define como nomear pastas, arquivos, tabelas e código do projeto.
Todo novo módulo deve seguir exatamente estas regras.

## 1. Regras gerais

| Regra | Exemplo correto | Evitar |
|-------|-----------------|--------|
| Tudo em minúsculas | `clientes_rotas.py` | `Clientes_Rotas.py` |
| Palavras separadas por `_` (snake_case) | `clientes_cadastro.html` | `clientesCadastro.html`, `clientes-cadastro.html` |
| Sem acentos, cedilha ou espaços | `migracoes/`, `validacao.py` | `migrações/`, `validação.py` |
| Nomes em português | `clientes_repositorio.py` | `customers_repository.py` |
| Módulos no plural | `clientes`, `fornecedores`, `produtos` | `cliente`, `fornecedor` |

**Exceções:** nomes exigidos por ferramentas ficam como a ferramenta espera:
`app/`, `static/`, `templates/`, `run.py`, `requirements.txt`, `README.md`,
`.gitignore`, `.env`, `pytest.ini` e arquivos de teste com prefixo `test_`.

## 2. Arquivos de um módulo

Todo arquivo de um módulo começa com o nome do módulo: **`<modulo>_<papel>.<extensão>`**.
Assim, com várias abas abertas no editor, fica claro de qual módulo é cada arquivo.

| Camada | Local | Nome |
|--------|-------|------|
| Rotas (URLs) | `app/modulos/<modulo>/` | `<modulo>_rotas.py` |
| Acesso ao banco (SQL) | `app/modulos/<modulo>/` | `<modulo>_repositorio.py` |
| Regras de validação | `app/modulos/<modulo>/` | `<modulo>_validacao.py` |
| Tela | `app/templates/<modulo>/` | `<modulo>_<tela>.html` |
| JavaScript da tela | `app/static/js/<modulo>/` | `<modulo>_<tela>.js` |
| CSS da tela (só se precisar) | `app/static/css/<modulo>/` | `<modulo>_<tela>.css` |
| Testes | `testes/` | `test_<modulo>_<papel>.py` |

O HTML, o JS e o CSS de uma mesma tela têm **o mesmo nome**, mudando só a extensão:
`clientes_cadastro.html` ↔ `clientes_cadastro.js` ↔ `clientes_cadastro.css`.

## 3. Código compartilhado (`comum/`)

O que serve a mais de um módulo fica em uma pasta `comum/`, sem prefixo de módulo:

- `app/comum/validadores.py` e `app/static/js/comum/validadores.js` (mesmas regras nos dois lados)
- `app/comum/erros.py`
- `app/templates/comum/base.html`
- `app/static/css/comum/base.css`, `formularios.css`, `tabelas.css`
- `app/static/js/comum/api.js`, `aviso.js`, `formulario.js`, `mascaras.js`

Regra prática: se um trecho de código for copiado para um segundo módulo, ele deve ir para `comum/`.

## 4. Banco de dados

| Item | Padrão | Exemplo |
|------|--------|---------|
| Banco | minúsculas, snake_case | `projeto_utilizando_ia` |
| Tabelas | minúsculas, plural, snake_case | `clientes`, `itens_pedido` |
| Colunas | minúsculas, singular, snake_case | `nome`, `data_cadastro` |
| Chave primária | `id` | `id` |
| Chave estrangeira | `<tabela_no_singular>_id` | `cliente_id` |
| Migrações | `NNN_<acao>_<objeto>.sql` | `001_criar_tabela_clientes.sql`, `002_adicionar_coluna_cpf_clientes.sql` |
| Dados de exemplo | `NNN_<tabela>.sql` | `001_clientes.sql` |

- Tabelas em minúsculas evitam erro ao publicar em servidor Linux, onde o MySQL
  diferencia `Clientes` de `clientes` (no Windows não diferencia).
- **Migrações já executadas nunca são editadas.** Toda mudança vira um novo arquivo com o próximo número.

## 5. Código

| Linguagem | Item | Padrão | Exemplo |
|-----------|------|--------|---------|
| Python | funções e variáveis | snake_case | `validar_email`, `cliente_id` |
| Python | classes | PascalCase | `RegistroDuplicadoErro` |
| Python | constantes | MAIÚSCULAS | `ERRO_DUPLICADO` |
| JavaScript | funções e variáveis | camelCase | `validarEmail`, `idEmEdicao` |
| JavaScript | constantes fixas | MAIÚSCULAS | `API`, `COLUNAS` |
| HTML/CSS | ids e classes | kebab-case | `form-cliente`, `btn-salvar` |
| Flask | blueprint | `<modulo>_bp` | `clientes_bp` |

## 6. URLs

| Tipo | Padrão | Exemplo |
|------|--------|---------|
| Tela | `/<modulo>` | `/clientes` |
| API — listar / cadastrar | `/api/<modulo>` | `GET` / `POST /api/clientes` |
| API — alterar um registro | `/api/<modulo>/<id>` | `PUT /api/clientes/5` |

## 7. Checklist: criando um novo módulo (ex.: `fornecedores`)

1. `banco_dados/migracoes/002_criar_tabela_fornecedores.sql`
2. `app/modulos/fornecedores/__init__.py` (vazio)
3. `app/modulos/fornecedores/fornecedores_validacao.py`
4. `app/modulos/fornecedores/fornecedores_repositorio.py`
5. `app/modulos/fornecedores/fornecedores_rotas.py` com `fornecedores_bp`
6. Registrar `fornecedores_bp` em `app/__init__.py`
7. `app/templates/fornecedores/fornecedores_cadastro.html` (estendendo `comum/base.html`)
8. `app/static/js/fornecedores/fornecedores_cadastro.js`
9. `testes/test_fornecedores_validacao.py`
