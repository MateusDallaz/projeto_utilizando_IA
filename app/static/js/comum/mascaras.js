// ============================================================
// mascaras.js — formatação automática enquanto o usuário digita
// ============================================================

/** 47999991111 -> (47) 99999-1111 | 4733331111 -> (47) 3333-1111 */
export function mascaraTelefone(valor) {
  const d = valor.replace(/\D/g, "").slice(0, 11);
  if (d.length === 0) return "";
  if (d.length <= 2) return `(${d}`;
  if (d.length <= 6) return `(${d.slice(0, 2)}) ${d.slice(2)}`;
  if (d.length <= 10) return `(${d.slice(0, 2)}) ${d.slice(2, 6)}-${d.slice(6)}`;
  return `(${d.slice(0, 2)}) ${d.slice(2, 7)}-${d.slice(7)}`;
}

/** Remove qualquer espaço (útil para e-mail). */
export function semEspacos(valor) {
  return valor.replace(/\s/g, "");
}
