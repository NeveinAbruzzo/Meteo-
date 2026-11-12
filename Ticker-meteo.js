document.addEventListener("DOMContentLoaded", function () {
  // 1. Aggiunge gli stili CSS del tuo ticker (utili per le pagine che non li hanno già)
  const style = document.createElement("style");
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

  // 2. Se la pagina non ha ancora la .ticker-bar, la inserisce subito sotto la .navbar (o in cima alla pagina)
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

  // 3. Scarica i dati aggiornati da GitHub e popola sia il ticker sia i riquadri riepilogo (se presenti)
  const urlDati = "https://githubusercontent.com" + new Date().getTime();

  fetch(urlDati)
    .then((res) => {
      if (!res.ok) throw new Error("Errore caricamento Dati_meteo.txt");
      return res.text();
    })
    .then((testo) => {
      const righe = testo.split("\n");
      let htmlTicker = "";
      let stazioni = [];
      let ultimoAggiornamento = "";

      righe.forEach((riga) => {
        const pulita = riga.trim();
        if (!pulita) return;

        if (pulita.startsWith("===")) {
          ultimoAggiornamento = pulita.replace(/=/g, "").trim();
        } else if (pulita.includes(":")) {
          const [citta, tempStr] = pulita.split(":");
          const nomeCitta = citta.trim();
          const valoreTemp = tempStr.trim();

          htmlTicker += `<span class="ticker-item"><span class="city">${nomeCitta}:</span> <span class="temp">${valoreTemp}</span></span>`;

          const numTemp = parseFloat(valoreTemp.replace("°C", ""));
          if (!isNaN(numTemp)) {
            stazioni.push({ nome: nomeCitta, temp: numTemp, testo: valoreTemp });
          }
        }
      });

      tickerContent.innerHTML = htmlTicker || "Dati meteo non disponibili";

      // Aggiorna l'orario nell'header se presente nella pagina
      const updateTimeEl = document.getElementById("update-time");
      if (updateTimeEl && ultimoAggiornamento) {
        updateTimeEl.textContent = ultimoAggiornamento;
      }

      // Aggiorna anche il riquadro "Estremi Rilevati" nella Home se presente
      if (stazioni.length > 0) {
        const piuCalda = stazioni.reduce((a, b) => (a.temp > b.temp ? a : b));
        const piuFredda = stazioni.reduce((a, b) => (a.temp < b.temp ? a : b));

        const maxEl = document.getElementById("max-city");
        const minEl = document.getElementById("min-city");
        const countEl = document.getElementById("active-stations");

        if (maxEl) maxEl.textContent = `${piuCalda.nome} (${piuCalda.testo})`;
        if (minEl) minEl.textContent = `${piuFredda.nome} (${piuFredda.testo})`;
        if (countEl) countEl.textContent = stazioni.length;
      }
    })
    .catch((err) => {
      console.error("Errore ticker meteo:", err);
      tickerContent.textContent = "Dati meteo temporaneamente non disponibili";
    });
});

