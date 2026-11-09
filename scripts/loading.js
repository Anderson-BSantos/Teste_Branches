function showLoading() {
    const div = document.createElement('div');
    div.classList.add('loading');
    document.body.appendChild(div);

    const label = document.createElement("label")
    label.innerHTML = "Carregando...";
    div.appendChild(label);

}
function hideLoading() {
    const loadings = document.getElementsByClassName('loading');

    if (loadings.length) {
        loadings[0].remove();
    }
}

function atualizarProgresso(percentual) {
    const bar = document.getElementById("progressBar");
    bar.style.width = percentual + "%";
  }
  
  // Exemplo de simulação:
  let progresso = 0;
  const interval = setInterval(() => {
    if (progresso >= 100) {
      clearInterval(interval);
    } else {
      progresso += 10;
      atualizarProgresso(progresso);
    }
  }, 300);