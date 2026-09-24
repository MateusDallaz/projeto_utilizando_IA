// ============================================================
// clientes_cadastro.js — tela de cadastro e alteração de clientes
// ============================================================

import { requisitar } from "../comum/api.js";
import { avisar } from "../comum/aviso.js";
import { criarEtapas } from "../comum/etapas.js";
import { criarControleFormulario } from "../comum/formulario.js";
import { mascaraTelefone, semEspacos } from "../comum/mascaras.js";
import {
  normalizarBusca,
  validarEmail,
  validarNomeLugar,
  validarNomePessoa,
  validarTelefone,
} from "../comum/validadores.js";

const API = "/api/clientes";

const form = document.getElementById("form-cliente");
const ficha = document.querySelector(".ficha");
const tituloFicha = document.getElementById("titulo-ficha");
const seloModo = document.getElementById("modo");
const btnSalvar = document.getElementById("btn-salvar");
const btnCancelar = document.getElementById("btn-cancelar");
const tabela = document.getElementById("tabela-clientes");
const listaVazia = document.getElementById("lista-vazia");
const contador = document.getElementById("contador");
const busca = document.getElementById("busca");

const formulario = criarControleFormulario(
  form,
  {
    nome: validarNomePessoa,
    email: validarEmail,
    telefone: validarTelefone,
    cidade: validarNomeLugar,
  },
  {
    mascaras: { telefone: mascaraTelefone, email: semEspacos },
    erroGeral: document.getElementById("erro-geral"),
  }
);

// Um campo habilitado por vez: nome -> e-mail -> telefone -> cidade
const etapas = criarEtapas(form, ["nome", "email", "telefone", "cidade"], {
  validarCampo: formulario.validarCampo,
  aoMudar: () => (btnSalvar.textContent = textoBotao()),
});

// Colunas exibidas na tabela: [campo, classe css opcional]
const COLUNAS = [["nome"], ["email", "quebra"], ["telefone", "numero"], ["cidade"]];

let clientes = [];
let idEmEdicao = null;
let enviando = false;

// ------------------------------------------------------------
// Modo cadastro / modo alteração
// ------------------------------------------------------------
function textoBotao() {
  if (!etapas.ultima()) return "Próximo";
  return idEmEdicao !== null ? "Salvar alterações" : "Cadastrar cliente";
}

function modoCadastro() {
  idEmEdicao = null;
  form.reset();
  formulario.limpar();
  ficha.classList.remove("editando");
  tituloFicha.textContent = "Novo cliente";
  seloModo.hidden = true;
  btnSalvar.textContent = textoBotao();
  btnCancelar.hidden = true;
  etapas.ir(0, { focar: false });
  renderizarTabela();
}

function modoAlteracao(cliente) {
  idEmEdicao = cliente.id;
  formulario.limpar();
  formulario.preencher(cliente);
  ficha.classList.add("editando");
  tituloFicha.textContent = cliente.nome;
  seloModo.hidden = false;
  btnSalvar.textContent = textoBotao();
  btnCancelar.hidden = false;
  etapas.ir(0, { focar: false });
  renderizarTabela();
  ficha.scrollIntoView({ behavior: "smooth", block: "start" });
  form.elements.nome.focus({ preventScroll: true });
}

btnCancelar.addEventListener("click", modoCadastro);

// ------------------------------------------------------------
// Envio (um cliente por vez)
// ------------------------------------------------------------
form.addEventListener("submit", async (evento) => {
  evento.preventDefault();
  if (enviando) return; // impede clique duplo / envio duplicado

  // Antes do último campo, Enter / "Próximo" só libera o campo seguinte
  if (!etapas.ultima()) {
    etapas.avancar();
    return;
  }

  formulario.mostrarErroGeral("");
  if (!formulario.validarTudo()) {
    etapas.irParaPrimeiroErro();
    return;
  }

  const editando = idEmEdicao !== null;
  enviando = true;
  btnSalvar.disabled = true;
  btnSalvar.textContent = editando ? "Salvando..." : "Cadastrando...";

  try {
    const { ok, corpo } = await requisitar(editando ? `${API}/${idEmEdicao}` : API, {
      metodo: editando ? "PUT" : "POST",
      dados: formulario.lerDados(),
    });

    if (!ok) {
      formulario.mostrarErrosServidor(corpo.erros || { geral: "Não foi possível salvar. Tente novamente." });
      etapas.irParaPrimeiroErro();
      return;
    }

    await carregarClientes(corpo.id);
    avisar(editando ? `Alterações de ${corpo.nome} salvas.` : `${corpo.nome} cadastrado.`);
    modoCadastro();
    form.elements.nome.focus();
  } catch {
    formulario.mostrarErroGeral("Sem conexão com o servidor. Verifique se o back end está rodando.");
  } finally {
    enviando = false;
    btnSalvar.disabled = false;
    btnSalvar.textContent = textoBotao();
  }
});

// ------------------------------------------------------------
// Lista de clientes
// ------------------------------------------------------------
async function carregarClientes(idDestaque = null) {
  try {
    const { ok, corpo } = await requisitar(API);
    if (!ok) throw new Error();
    clientes = corpo;
    renderizarTabela(idDestaque);
  } catch {
    tabela.replaceChildren();
    listaVazia.textContent = "Não foi possível carregar os clientes. Verifique a conexão com o banco.";
    listaVazia.hidden = false;
  }
}

function criarLinha(cliente, idDestaque) {
  const linha = document.createElement("tr");
  if (cliente.id === idEmEdicao) linha.classList.add("em-edicao");
  if (cliente.id === idDestaque) linha.classList.add("destaque");

  // textContent evita que dados do banco sejam interpretados como HTML
  COLUNAS.forEach(([campo, classe]) => {
    const td = document.createElement("td");
    td.textContent = cliente[campo] ?? "";
    if (classe) td.className = classe;
    linha.appendChild(td);
  });

  const tdAcao = document.createElement("td");
  const botao = document.createElement("button");
  botao.type = "button";
  botao.className = "btn-editar";
  botao.textContent = "Editar";
  botao.setAttribute("aria-label", `Editar ${cliente.nome}`);
  botao.addEventListener("click", () => modoAlteracao(cliente));
  tdAcao.appendChild(botao);
  linha.appendChild(tdAcao);
  return linha;
}

function renderizarTabela(idDestaque = null) {
  const termo = normalizarBusca(busca.value.trim());
  const filtrados = clientes.filter(
    (c) => !termo || [c.nome, c.email, c.cidade].some((v) => normalizarBusca(v).includes(termo))
  );

  contador.textContent = `(${clientes.length})`;
  tabela.replaceChildren(...filtrados.map((c) => criarLinha(c, idDestaque)));

  if (clientes.length === 0) {
    listaVazia.textContent = "Nenhum cliente cadastrado ainda. Use a ficha ao lado para cadastrar o primeiro.";
  } else if (filtrados.length === 0) {
    listaVazia.textContent = `Nenhum cliente encontrado para “${busca.value.trim()}”.`;
  }
  listaVazia.hidden = filtrados.length > 0;
}

busca.addEventListener("input", () => renderizarTabela());

etapas.ir(0, { focar: false });
carregarClientes();
