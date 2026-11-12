document.addEventListener("DOMContentLoaded", function () {
  // 1. Stile CSS della barra scorrevole
  const stile = document.createElement("style");
  stile.textContent = `
    .ticker-meteo-container {
      width: 100%;
      background-color: #0b3c5d;
      color: #ffffff;
      font-family: Arial, sans-serif;
      font-size: 15px;
      display: flex;
      align-items: center;
      overflow: hidden;
      height: 42px;
      border-bottom: 2px solid #328cc1;
      position: sticky;
      top: 0;
      z-index: 9999;
      box-shadow: 0 4px 10px rgba(0,0,0,0.25);
    }
    .ticker-meteo-label {
      background-color: #328cc1;
      padding: 0 15px;
      height: 100%;
      display: flex;
      align-items: center;
      font-weight: bold;
      font-size: 0.85rem;
      text-transform: uppercase;
      white-space: nowrap;
      z-index: 2;
      flex-shrink: 0;
    }
    .ticker-meteo-scroll {
      display: inline-block;
      white-space: nowrap;
      padding-left: 100%;
      font-weight: bold;
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

  // 2. Inserisce la barra subito dopo il menu nero (.navbar)
  const barra = document.createElement("div");
  barra.className = "ticker-meteo-container";
  barra.innerHTML = `
    <div class="ticker-meteo-label">TEMPERATURE LIVE:</div>
    <div class="ticker-meteo-scroll" id="testo-temperature-live">Caricamento dati live...</div>
  `;

  const navbar = document.querySelector(".navbar");
  if (navbar) {
    navbar.insertAdjacentElement("afterend", barra);
  } else {
    document.body.prepend(barra);
  }

  // 3. Stazioni meteo in tempo reale
  const localita = [
    { nome: "Roccaraso", lat: 41.8487, lon: 14.0785 },
    { nome: "Scanno", lat: 41.9044, lon: 13.8796 },
    { nome: "Frosinone", lat: 41.6398, lon: 13.3411 },
    { nome: "Pescocostanzo", lat: 41.8872, lon: 14.0661 },
    { nome: "Villetta Barrea", lat: 41.7554, lon: 13.9909 },
    { nome: "Chieti", lat: 42.3483, lon: 14.1649 },
    { nome: "Napoli", lat: 40.8762, lon: 14.5195 }
  ];

  function ottieniIcona(code) {
    if (code === 0) return "☀️";
    if (code >= 1 && code <= 3) return "⛅";
    if (code === 45 || code === 48) return "🌫️";
    if (code >= 51 && code <= 67) return "🌧️";
    if (code >= 71 && code <= 77) return "❄️";
    if (code >= 80 && code <= 82) return "🌦️";
    if (code >= 95) return "⛈️";
    return "☁️";
  }

  function descriviSituazione(code) {
    if (code === 0) return "cielo sereno e condizioni di piena stabilità atmosferica";
    if (code >= 1 && code <= 3) return "nuvolosità irregolare alternata ad ampie schiarite";
    if (code === 45 || code === 48) return "foschie dense o locali banchi di nebbia nelle valli";
    if (code >= 51 && code <= 67) return "condizioni di spiccata variabilità con piogge sparse";
    if (code >= 71 && code <= 77) return "precipitazioni nevose sui settori montani e appenninici";
    if (code >= 80 && code <= 82) return "rovesci sparsi localmente moderati";
    if (code >= 95) return "instabilità marcata con attività temporalesca in atto";
    return "nubi sparse sul comprensorio";
  }

  async function aggiornaTuttoInTempoReale() {
    try {
      const lats = localita.map(c => c.lat).join(",");
      const lons = localita.map(c => c.lon).join(",");
      const url = `https://open-meteo.com{lats}&longitude=${lons}&current=temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m&timezone=Europe%2FRome`;

      const response = await fetch(url);
      const dati = await response.json();

      let maxTemp = -999;
      let minTemp = 999;
      let cittaCalda = "";
      let cittaFredda = "";
      let sommaVento = 0;

      const stringheBarra = dati.map((item, i) => {
        const nome = localita[i].nome;
        const temp = item.current.temperature_2m;
        const code = item.current.weather_code;
        const vento = item.current.wind_speed_10m;

        sommaVento += vento;

        if (temp > maxTemp) {
          maxTemp = temp;
          cittaCalda = `${nome} (${temp}°C)`;
        }
        if (temp < minTemp) {
          minTemp = temp;
          cittaFredda = `${nome} (${temp}°C)`;
        }

        return `<span style="color:#efbc9b;">${nome}:</span> ${temp}°C ${ottieniIcona(code)}`;
      });

      // 1. Aggiorna barra scorrevole
      const elBarra = document.getElementById("testo-temperature-live");
      if (elBarra) {
        elBarra.innerHTML = stringheBarra.join(" &nbsp;&nbsp;&nbsp;&nbsp;•&nbsp;&nbsp;&nbsp;&nbsp; ");
      }

      // 2. Aggiorna orario
      const elOrario = document.getElementById("update-time");
      if (elOrario) {
        const adesso = new Date().toLocaleString("it-IT", {
          day: "2-digit", month: "2-digit", year: "numeric",
          hour: "2-digit", minute: "2-digit"
        });
        elOrario.textContent = `Ultimo aggiornamento in tempo reale: ${adesso}`;
      }

      // 3. Aggiorna Estremi Rilevati
      const elCalda = document.getElementById("max-city");
      const elFredda = document.getElementById("min-city");
      const elStazioni = document.getElementById("active-stations");

      if (elCalda) elCalda.textContent = cittaCalda;
      if (elFredda) elFredda.textContent = cittaFredda;
      if (elStazioni) elStazioni.textContent = localita.length;

      // 4. Aggiorna il Bollettino Meteorologico Generale IN TEMPO REALE
      const elBoll1 = document.getElementById("bollettino-testo-1");
      const elBoll2 = document.getElementById("bollettino-testo-2");

      if (elBoll1 && elBoll2) {
        // dati[0] è Roccaraso (Abruzzo interno), dati[5] è Chieti (Abruzzo costiero/collinare)
        const meteoMonti = descriviSituazione(dati[0].current.weather_code);
        const meteoCosta = descriviSituazione(dati[5].current.weather_code);
        const tempRoccaraso = dati[0].current.temperature_2m;
        const tempChieti = dati[5].current.temperature_2m;
        const umidita = dati[0].current.relative_humidity_2m;
        const ventoMedio = Math.round(sommaVento / dati.length);

        elBoll1.innerHTML = `In questo momento sull'Abruzzo si rileva <strong>${meteoMonti}</strong> sui settori montani (Roccaraso <strong>${tempRoccaraso}°C</strong>, umidità ${umidita}%) e <strong>${meteoCosta}</strong> verso la fascia adriatica e collinare (Chieti <strong>${tempChieti}°C</strong>).`;
        elBoll2.innerHTML = `Ventilazione media sul comprensorio intorno a <strong>${ventoMedio} km/h</strong>, con escursione termica attuale compresa tra i <strong>${minTemp}°C</strong> di ${cittaFredda.split(" ")[0]} e i <strong>${maxTemp}°C</strong> di ${cittaCalda.split(" ")[0]}.`;
      }

    } catch (errore) {
      console.error("Errore aggiornamento meteo:", errore);
    }
  }

  aggiornaTuttoInTempoReale();
  setInterval(aggiornaTuttoInTempoReale, 900000);
});
