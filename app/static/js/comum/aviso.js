// ============================================================
// aviso.js — mensagem de confirmação no rodapé da tela
// Requer <div id="aviso" class="aviso"> (já existe no base.html).
// ============================================================

let temporizador;

export function avisar(texto, falha = false) {
  const aviso = document.getElementById("aviso");
  clearTimeout(temporizador);
  aviso.textContent = texto;
  aviso.classList.toggle("falha", falha);
  aviso.classList.add("visivel");
  temporizador = setTimeout(() => aviso.classList.remove("visivel"), 3500);
}
