// ============================================================
// api.js — comunicação com o back end (usado por todos os módulos)
// Envia o token da tela aberta (X-Token). Se a sessão acabou,
// volta para a tela de login.
// ============================================================

const TOKEN = document.querySelector('meta[name="token-tela"]')?.content ?? "";

function irParaLogin() {
  window.location.replace("/login");
}

// Voltar/avançar do navegador pode reexibir a tela guardada em memória
// sem passar pelo servidor: nesse caso, exige o login de novo.
window.addEventListener("pageshow", (evento) => {
  if (evento.persisted) irParaLogin();
});

/**
 * Faz uma requisição JSON.
 * Retorna { ok, status, corpo }. Lança erro apenas se não houver conexão.
 */
export async function requisitar(url, { metodo = "GET", dados } = {}) {
  const opcoes = { method: metodo, headers: { "X-Token": TOKEN } };
  if (dados !== undefined) {
    opcoes.headers["Content-Type"] = "application/json";
    opcoes.body = JSON.stringify(dados);
  }
  const resposta = await fetch(url, opcoes);
  if (resposta.status === 401) {
    irParaLogin();
    return new Promise(() => {}); // a página vai ser trocada; não continua o fluxo
  }
  const corpo = await resposta.json().catch(() => ({}));
  return { ok: resposta.ok, status: resposta.status, corpo };
}
