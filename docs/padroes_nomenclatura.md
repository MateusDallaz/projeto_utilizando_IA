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

**Exceções:**
- As três pastas de camada usam inicial maiúscula: `View/`, `Control/` e `Model/`.
- Nomes exigidos por ferramentas ficam como a ferramenta espera:
  `static/`, `templates/`, `run.py`, `requirements.txt`, `README.md`, `.gitignore`, `.env`.

## 2. Arquivos de um módulo

Todo arquivo de um módulo começa com o nome do módulo: **`<modulo>_<papel>.<extensão>`**.
Assim, com várias abas abertas no editor, fica claro de qual módulo é cada arquivo.

| Camada | Local | Nome |
|--------|-------|------|
| Rotas (URLs) | `Control/<modulo>/` | `<modulo>_rotas.py` |
| Regras de validação | `Control/<modulo>/` | `<modulo>_validacao.py` |
| Acesso ao banco (SQL) | `Model/<modulo>/` | `<modulo>_repositorio.py` |
| Tela | `View/templates/<modulo>/` | `<modulo>_<tela>.html` |
| JavaScript da tela | `View/static/js/<modulo>/` | `<modulo>_<tela>.js` |
| CSS da tela (só se precisar) | `View/static/css/<modulo>/` | `<modulo>_<tela>.css` |

Regra das camadas: **View** só conversa com o back end pela API; **Control** valida e chama o
**Model**; só o **Model** tem SQL. O Model nunca importa nada do Control.

O HTML, o JS e o CSS de uma mesma tela têm **o mesmo nome**, mudando só a extensão:
`clientes_cadastro.html` ↔ `clientes_cadastro.js` ↔ `clientes_cadastro.css`.

## 3. Código compartilhado (`comum/`)

O que serve a mais de um módulo fica em uma pasta `comum/` (ou na raiz do `Model/`), sem prefixo de módulo:

- `Control/comum/validadores.py` e `View/static/js/comum/validadores.js` (mesmas regras nos dois lados)
- `Model/conexao.py` e `Model/erros.py`
- `View/templates/comum/base.html`
- `View/static/css/comum/base.css`, `formularios.css`, `tabelas.css`
- `View/static/js/comum/api.js`, `aviso.js`, `etapas.js`, `formulario.js`, `mascaras.js`

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

1. `Model/migracoes/002_criar_tabela_fornecedores.sql`
2. `Model/fornecedores/__init__.py` (vazio) e `Model/fornecedores/fornecedores_repositorio.py`
3. `Control/fornecedores/__init__.py` (vazio) e `Control/fornecedores/fornecedores_validacao.py`
4. `Control/fornecedores/fornecedores_rotas.py` com `fornecedores_bp`
   (rota da tela com `@tela_protegida` e rotas da API com `@api_protegida`)
5. Registrar `fornecedores_bp` em `Control/__init__.py`
6. `View/templates/fornecedores/fornecedores_cadastro.html` (estendendo `comum/base.html`)
7. `View/static/js/fornecedores/fornecedores_cadastro.js`
