// ============================================================
// etapas.js — preenchimento campo a campo
// Só um campo fica habilitado por vez. O próximo só é liberado
// quando o atual está válido (Enter, Tab ou botão "Próximo").
// Clicar em um campo já preenchido volta para ele.
// Shift+Tab volta para o campo anterior.
// ============================================================

export function criarEtapas(form, campos, { validarCampo, aoMudar } = {}) {
  const bloco = (campo) => form.querySelector(`[data-campo="${campo}"]`);
  let atual = 0;

  const ultima = () => atual === campos.length - 1;

  /** Habilita somente o campo de índice `indice`. */
  function ir(indice, { focar = true } = {}) {
    atual = indice;
    campos.forEach((campo, i) => {
      form.elements[campo].disabled = i !== atual;
      bloco(campo).classList.toggle("atual", i === atual);
      bloco(campo).classList.toggle("concluido", i < atual);
      bloco(campo).classList.toggle("pendente", i > atual);
    });
    if (focar) form.elements[campos[atual]].focus();
    if (aoMudar) aoMudar();
  }

  /** Valida o campo atual e, se estiver ok, libera o próximo. Retorna true se válido. */
  function avancar() {
    const campo = campos[atual];
    if (!validarCampo(campo)) {
      form.elements[campo].focus();
      return false;
    }
    if (!ultima()) ir(atual + 1);
    return true;
  }

  /** Volta para o primeiro campo marcado com erro (ex.: erro devolvido pelo back end). */
  function irParaPrimeiroErro() {
    const indice = campos.findIndex((c) => bloco(c).classList.contains("invalido"));
    if (indice !== -1) ir(indice);
  }

  campos.forEach((campo, i) => {
    form.elements[campo].addEventListener("keydown", (evento) => {
      if (evento.key !== "Tab") return;
      if (evento.shiftKey) {
        if (i > 0) {
          evento.preventDefault();
          ir(i - 1);
        }
        return;
      }
      if (ultima()) return; // no último campo o Tab segue para o botão
      evento.preventDefault();
      avancar();
    });

    bloco(campo).addEventListener("click", () => {
      if (i < atual) ir(i);
    });
  });

  return { ir, avancar, ultima, irParaPrimeiroErro };
}
