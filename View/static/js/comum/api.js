// ============================================================
// api.js — comunicação com o back end (usado por todos os módulos)
// ============================================================

/**
 * Faz uma requisição JSON.
 * Retorna { ok, status, corpo }. Lança erro apenas se não houver conexão.
 */
export async function requisitar(url, { metodo = "GET", dados } = {}) {
  const opcoes = { method: metodo, headers: {} };
  if (dados !== undefined) {
    opcoes.headers["Content-Type"] = "application/json";
    opcoes.body = JSON.stringify(dados);
  }
  const resposta = await fetch(url, opcoes);
  const corpo = await resposta.json().catch(() => ({}));
  return { ok: resposta.ok, status: resposta.status, corpo };
}
