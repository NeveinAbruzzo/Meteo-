document.addEventListener("DOMContentLoaded", function () {
  // 1. Aggiunge lo stile CSS per lo scorrimento continuo e la barra fissa in alto
  const stile = document.createElement("style");
  stile.textContent = `
    .ticker-meteo-container {
      width: 100%;
      background-color: #1565c0;
      color: #ffffff;
      font-family: Arial, sans-serif;
      font-size: 14px;
      display: flex;
      align-items: center;
      overflow: hidden;
      height: 36px;
      position: sticky;
      top: 0;
      z-index: 1000;
      box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    .ticker-meteo-label {
      background-color: #0d47a1;
      padding: 0 15px;
      height: 100%;
      display: flex;
      align-items: center;
      font-weight: bold;
      white-space: nowrap;
      z-index: 2;
    }
    .ticker-meteo-scroll {
      display: inline-block;
      white-space: nowrap;
      padding-left: 100%;
      animation: scorrimento-meteo 28s linear infinite;
    }
    .ticker-meteo-container:hover .ticker-meteo-scroll {
      animation-play-state: paused;
    }
    @keyframes scorrimento-meteo {
      0% { transform: translateX(0); }
      100% { transform: translateX(-100%); }
    }
  `;
  document.head.appendChild(stile);

  // 2. Crea l'elemento HTML della barra
  const barra = document.createElement("div");
  barra.className = "ticker-meteo-container";
  barra.innerHTML = `
    <div class="ticker-meteo-label">TEMPERATURE LIVE:</div>
    <div class="ticker-meteo-scroll" id="testo-temperature-live">Caricamento temperature...</div>
  `;

  // 3. Posiziona la barra subito dopo il menu di navigazione (nav)
  const nav = document.querySelector("nav");
  if (nav) {
    nav.insertAdjacentElement("afterend", barra);
  } else {
    document.body.prepend(barra);
  }

  // 4. Legge il file Dati_meteo.txt aggiornato dal tuo script Python
  // Il parametro ?t=... evita che il browser mostri vecchi dati salvati in cache
  fetch("Dati_meteo.txt?t=" + new Date().getTime())
    .then((response) => {
      if (!response.ok) throw new Error("File non trovato");
      return response.text();
    })
    .then((testo) => {
      const righe = testo.split("\n");
      const listaCitta = [];

      righe.forEach((riga) => {
        const pulita = riga.trim();
        // Salta righe vuote e l'intestazione === ULTIMO AGGIORNAMENTO...
        if (pulita && !pulita.startsWith("===")) {
          listaCitta.push(`${pulita} ☁️`);
        }
      });

      const contenitoreTesto = document.getElementById("testo-temperature-live");
      if (listaCitta.length > 0) {
        contenitoreTesto.innerHTML = listaCitta.join(" &nbsp;&nbsp;&nbsp;•&nbsp;&nbsp;&nbsp; ");
      } else {
        contenitoreTesto.textContent = "Dati meteo momentaneamente non disponibili.";
      }
    })
    .catch((errore) => {
      console.error("Errore caricamento Dati_meteo.txt:", errore);
      document.getElementById("testo-temperature-live").textContent = "Errore caricamento dati meteo.";
    });
});

