
document.addEventListener("DOMContentLoaded", function () {
  // 1. Aggiunge gli stili CSS del ticker se non già presenti
  if (!document.getElementById("ticker-bar-styles")) {
    const style = document.createElement("style");
    style.id = "ticker-bar-styles";
    style.textContent = `
      .ticker-bar { background-color: #0b3c5d; color: white; overflow: hidden; white-space: nowrap; display: flex; align-items: center; border-bottom: 2px solid #328cc1; height: 42px; font-family: Arial, sans-serif; }
      .ticker-title { background-color: #328cc1; padding: 0 15px; height: 100%; display: flex; align-items: center; font-weight: bold; font-size: 0.85rem; text-transform: uppercase; z-index: 2; flex-shrink: 0; }
      .ticker-wrap { width: 100%; overflow: hidden; }
      .ticker-move { display: inline-block; white-space: nowrap; padding-left: 100%; animation: tickerEffect 35s linear infinite; }
      .ticker-move:hover { animation-play-state: paused; }
      .ticker-item { display: inline-block; padding: 0 25px; font-size: 0.95rem; }
      .ticker-item .city { font-weight: bold; color: #efbc9b; }
      .ticker-item .temp { font-weight: bold; color: #fff; }
      @keyframes tickerEffect { 0% { transform: translate3d(0, 0, 0); } 100% { transform: translate3d(-100%, 0, 0); } }
    `;
    document.head.appendChild(style);
  }

  // 2. Inserisce la .ticker-bar se non già presente
  let tickerContent = document.getElementById("ticker-content");
  if (!tickerContent) {
    const tickerBar = document.createElement("div");
    tickerBar.className = "ticker-bar";
    tickerBar.innerHTML = `
      <div class="ticker-title">Temperature Live:</div>
      <div class="ticker-wrap">
        <div class="ticker-move" id="ticker-content">Caricamento dati meteo in tempo reale...</div>
      </div>
    `;

    const navbar = document.querySelector(".navbar");
    if (navbar) {
      navbar.insertAdjacentElement("afterend", tickerBar);
    } else {
      document.body.prepend(tickerBar);
    }
    tickerContent = document.getElementById("ticker-content");
  }

  // 3. Sostituisci con l'URL raw reale del tuo file Dati_meteo.txt su GitHub
  const baseUrl = "https://raw.githubusercontent.com/UTENTE/REPO/BRANCH/Dati_meteo.txt";
  const sep = baseUrl.includes("?") ? "&" : "?";
  const urlDati = `${baseUrl}${sep}t=${Date.now()}`;

  fetch(urlDati)
    .then((res) => {
      if (!res.ok) {
        throw new Error(`Errore HTTP ${res.status} nel caricamento di Dati_meteo.txt`);
      }
      return res.text();
    })
    .then((testo) => {
      const righe = testo.split(/\r?\n/);
      let htmlTicker = "";
      const stazioni = [];
      let ultimoAggiornamento = "";

      righe.forEach((riga) => {
        const pulita = riga.trim();
        if (!pulita) return;

        if (pulita.startsWith("===")) {
          ultimoAggiornamento = pulita.replace(/=/g, "").trim();
        } else if (pulita.includes(":")) {
          const idx = pulita.indexOf(":");
          const nomeCitta = pulita.slice(0, idx).trim();
          const valoreTemp = pulita.slice(idx + 1).trim();

          if (!nomeCitta || !valoreTemp) return;

          htmlTicker += `<span class="ticker-item"><span class="city">${escapeHtml(nomeCitta)}:</span> <span class="temp">${escapeHtml(valoreTemp)}</span></span>`;

          const matchNum = valoreTemp.replace(",", ".").match(/-?\d+(\.\d+)?/);
          const numTemp = matchNum ? parseFloat(matchNum[0]) : NaN;
          if (!isNaN(numTemp)) {
            stazioni.push({ nome: nomeCitta, temp: numTemp, testo: valoreTemp });
          }
        }
      });

      if (htmlTicker) {
        if (ultimoAggiornamento) {
          htmlTicker += `<span class="ticker-item"><span class="city">Aggiornamento:</span> <span class="temp">${escapeHtml(ultimoAggiornamento)}</span></span>`;
        }
        tickerContent.innerHTML = htmlTicker;
      } else {
        tickerContent.textContent = "Nessun dato meteo disponibile al momento.";
      }

      // 4. Aggiorna eventuali riquadri di riepilogo presenti nella pagina
      aggiornaRiepilogo(stazioni, ultimoAggiornamento);
    })
    .catch((err) => {
      console.error(err);
      tickerContent.textContent = "Impossibile caricare i dati meteo in tempo reale.";
    });

  function aggiornaRiepilogo(stazioni, ultimoAggiornamento) {
    const updateEl = document.getElementById("meteo-ultimo-aggiornamento");
    if (updateEl && ultimoAggiornamento) {
      updateEl.textContent = ultimoAggiornamento;
    }

    const summaryContainer = document.getElementById("meteo-riepilogo");
    if (summaryContainer && stazioni.length > 0) {
      summaryContainer.innerHTML = stazioni
        .map(
          (s) =>
            `<div class="meteo-card"><strong>${escapeHtml(s.nome)}</strong>: <span>${escapeHtml(s.testo)}</span></div>`
        )
        .join("");
    }
  }

  function escapeHtml(str) {
    return str
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }
});

