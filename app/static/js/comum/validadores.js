// ============================================================
// validadores.js — mesmas regras de app/comum/validadores.py
// Cada função devolve "" (válido) ou a mensagem de erro.
// A validação no navegador só orienta; o back end valida de novo.
// ============================================================

const LETRAS = "A-Za-zÀ-ÖØ-öø-ÿ";
const PALAVRAS_RE = new RegExp(`^[${LETRAS}]+(?:[ '\\-][${LETRAS}]+)*$`);
const EMAIL_RE = /^[a-z0-9._%+\-]+@[a-z0-9\-]+(\.[a-z0-9\-]+)*\.[a-z]{2,}$/;

export const limparEspacos = (v) => v.trim().replace(/\s+/g, " ");

/** Minúsculas e sem acentos, para comparar textos na busca. */
export const normalizarBusca = (v) =>
  (v || "").normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();

export function validarNomePessoa(v) {
  const nome = limparEspacos(v);
  if (!nome) return "Informe o nome completo.";
  if (nome.length < 3 || nome.length > 100) return "O nome deve ter entre 3 e 100 caracteres.";
  if (!PALAVRAS_RE.test(nome)) return "Use apenas letras no nome, sem números ou símbolos.";
  if (nome.split(" ").length < 2) return "Informe nome e sobrenome.";
  return "";
}

export function validarEmail(v) {
  const email = v.trim().toLowerCase();
  if (!email) return "Informe o e-mail.";
  if (email.length > 150) return "O e-mail deve ter no máximo 150 caracteres.";
  if (email.includes(" ") || email.includes("..") || !EMAIL_RE.test(email))
    return "E-mail inválido. Exemplo correto: nome@empresa.com.br";
  return "";
}

export function validarTelefone(v) {
  const d = v.replace(/\D/g, "");
  if (!d) return "Informe o telefone.";
  if (d.length !== 10 && d.length !== 11) return "O telefone deve ter DDD + número (10 ou 11 dígitos).";
  if (d[0] === "0" || d[1] === "0") return "DDD inválido. Use dois dígitos, sem o zero: 47, 11, 48...";
  if (d.length === 11 && d[2] !== "9") return "Celular com 11 dígitos deve começar com 9 após o DDD.";
  return "";
}

export function validarNomeLugar(v) {
  const lugar = limparEspacos(v);
  if (!lugar) return "Informe a cidade.";
  if (lugar.length < 2 || lugar.length > 100) return "A cidade deve ter entre 2 e 100 caracteres.";
  if (!PALAVRAS_RE.test(lugar)) return "Use apenas letras na cidade, sem a sigla do estado.";
  return "";
}
