// ============================================================
// formulario.js — marcação de erros e validação ao digitar
// Funciona com qualquer formulário que siga a estrutura:
//   <div class="campo" data-campo="X"> <input name="X"> <p id="erro-X"> </div>
// ============================================================

export function criarControleFormulario(form, regras, { mascaras = {}, erroGeral } = {}) {
  const campos = Object.keys(regras);
  const bloco = (campo) => form.querySelector(`[data-campo="${campo}"]`);

  function marcar(campo, mensagem) {
    const input = form.elements[campo];
    document.getElementById(`erro-${campo}`).textContent = mensagem;
    bloco(campo).classList.toggle("invalido", Boolean(mensagem));
    bloco(campo).classList.toggle("valido", !mensagem && input.value.trim() !== "");
    input.setAttribute("aria-invalid", mensagem ? "true" : "false");
  }

  function validarCampo(campo) {
    const mensagem = regras[campo](form.elements[campo].value);
    marcar(campo, mensagem);
    return !mensagem;
  }

  /** Valida tudo; foca o primeiro campo com erro. Retorna true se estiver ok. */
  function validarTudo() {
    const resultados = campos.map(validarCampo);
    const primeiroErro = campos.find((_, i) => !resultados[i]);
    if (primeiroErro) form.elements[primeiroErro].focus();
    return !primeiroErro;
  }

  function mostrarErroGeral(mensagem) {
    if (!erroGeral) return;
    erroGeral.textContent = mensagem || "";
    erroGeral.hidden = !mensagem;
  }

  /** Mostra os erros devolvidos pelo back end: { campo: mensagem, geral: mensagem } */
  function mostrarErrosServidor(erros) {
    Object.entries(erros).forEach(([campo, msg]) =>
      campos.includes(campo) ? marcar(campo, msg) : mostrarErroGeral(msg)
    );
    const campoComErro = campos.find((c) => erros[c]);
    if (campoComErro) form.elements[campoComErro].focus();
  }

  function limpar() {
    campos.forEach((c) => {
      marcar(c, "");
      bloco(c).classList.remove("valido");
    });
    mostrarErroGeral("");
  }

  function lerDados() {
    return Object.fromEntries(campos.map((c) => [c, form.elements[c].value]));
  }

  function preencher(registro) {
    campos.forEach((c) => (form.elements[c].value = registro[c] ?? ""));
  }

  // Valida ao sair do campo; depois do primeiro erro, valida enquanto digita
  campos.forEach((campo) => {
    const input = form.elements[campo];
    input.addEventListener("blur", () => {
      if (input.value.trim() !== "") validarCampo(campo);
    });
    input.addEventListener("input", () => {
      if (mascaras[campo]) input.value = mascaras[campo](input.value);
      if (bloco(campo).classList.contains("invalido")) validarCampo(campo);
    });
  });

  return { validarCampo, validarTudo, mostrarErroGeral, mostrarErrosServidor, limpar, lerDados, preencher };
}
