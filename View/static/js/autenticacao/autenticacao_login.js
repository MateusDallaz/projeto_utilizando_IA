// ============================================================
// autenticacao_login.js — tela de login
// Confere se os campos foram preenchidos e evita envio duplicado.
// Usuário e senha são conferidos no back end.
// ============================================================

const form = document.getElementById("form-login");
const usuario = document.getElementById("usuario");
const senha = document.getElementById("senha");
const erro = document.getElementById("erro-login");
const btnEntrar = document.getElementById("btn-entrar");

function mostrarErro(mensagem, campo) {
  erro.textContent = mensagem;
  erro.hidden = false;
  campo.focus();
}

form.addEventListener("submit", (evento) => {
  if (!usuario.value.trim()) {
    evento.preventDefault();
    return mostrarErro("Informe o usuário.", usuario);
  }
  if (!senha.value) {
    evento.preventDefault();
    return mostrarErro("Informe a senha.", senha);
  }
  btnEntrar.disabled = true;
  btnEntrar.textContent = "Entrando...";
});

// Voltar para esta tela pelo navegador reabilita o botão
window.addEventListener("pageshow", () => {
  btnEntrar.disabled = false;
  btnEntrar.textContent = "Entrar";
});
