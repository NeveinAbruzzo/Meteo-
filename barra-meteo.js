document.addEventListener("DOMContentLoaded", function () {
  const stile = document.createElement("style");
  stile.textContent = `
    .ticker-meteo-container {
      width: 100%;
      background-color: #0b3c5d;
      color: #ffffff;
      font-family: Arial, sans-serif;
      font-size: 16px;
      display: flex;
      align-items: center;
      overflow: hidden;
      height: 44px;
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
      font-size: 14px;
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
      animation: scorrimento-meteo 40s linear infinite;
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

  const barra = document.createElement("div");
  barra.className = "ticker-meteo-container";
  barra.innerHTML = `
    <div class="ticker-meteo-label">TEMPERATURE LIVE ABRUZZO:</div>
    <div class="ticker-meteo-scroll" id="testo-temperature-live">Caricamento temperature live Abruzzo...</div>
  `;

  const navbar = document.querySelector(".navbar");
  if (navbar) {
    navbar.insertAdjacentElement("afterend", barra);
  } else {
    document.body.prepend(barra);
  }

  const localitaAbruzzo = [
    { nome: "L'Aquila", lat: 42.3507, lon: 13.3999 },
    { nome: "Pescara", lat: 42.4618, lon: 14.2161 },
    { nome: "Chieti", lat: 42.3483, lon: 14.1649 },
    { nome: "Teramo", lat: 42.6589, lon: 13.7044 },
    { nome: "Avezzano", lat: 42.0312, lon: 13.4262 },
    { nome: "Sulmona", lat: 42.0494, lon: 13.9255 },
    { nome: "Vasto", lat: 42.1118, lon: 14.7082 },
    { nome: "Lanciano", lat: 42.2266, lon: 14.3906 },
    { nome: "Roccaraso", lat: 41.8487, lon: 14.0785 },
    { nome: "Scanno", lat: 41.9044, lon: 13.8796 },
    { nome: "Pescocostanzo", lat: 41.8872, lon: 14.0661 },
    { nome: "Villetta Barrea", lat: 41.7554, lon: 13.9909 }
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
      const lats = localitaAbruzzo.map(c => c.lat).join(",");
      const lons = localitaAbruzzo.map(c => c.lon).join(",");
      const url = `https://open-meteo.com{lats}&longitude=${lons}&current=temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m&timezone=Europe%2FRome`;

      const response = await fetch(url);
      const dati = await response.json();

      let maxTemp = -999;
      let minTemp = 999;
      let cittaCalda = "";
      let cittaFredda = "";
      let nomeCalda = "";
      let nomeFredda = "";
      let sommaVento = 0;

      const stringheBarra = dati.map((item, i) => {
        const nome = localitaAbruzzo[i].nome;
        const temp = item.current.temperature_2m;
        const code = item.current.weather_code;
        const vento = item.current.wind_speed_10m;

        sommaVento += vento;

        if (temp > maxTemp) {
          maxTemp = temp;
          nomeCalda = nome;
          cittaCalda = `${nome} (${temp}°C)`;
        }
        if (temp < minTemp) {
          minTemp = temp;
          nomeFredda = nome;
          cittaFredda = `${nome} (${temp}°C)`;
        }

        return `<span style="color:#efbc9b;">${nome}:</span> ${temp}°C ${ottieniIcona(code)}`;
      });

      const elBarra = document.getElementById("testo-temperature-live");
      if (elBarra) {
        elBarra.innerHTML = stringheBarra.join(" &nbsp;&nbsp;&nbsp;&nbsp;•&nbsp;&nbsp;&nbsp;&nbsp; ");
      }

      const elOrario = document.getElementById("update-time");
      if (elOrario) {
        const adesso = new Date().toLocaleString("it-IT", {
          day: "2-digit", month: "2-digit", year: "numeric",
          hour: "2-digit", minute: "2-digit"
        });
        elOrario.textContent = `Ultimo aggiornamento in tempo reale: ${adesso}`;
      }

      const elCalda = document.getElementById("max-city");
      const elFredda = document.getElementById("min-city");
      const elStazioni = document.getElementById("active-stations");

      if (elCalda) elCalda.textContent = cittaCalda;
      if (elFredda) elFredda.textContent = cittaFredda;
      if (elStazioni) elStazioni.textContent = localitaAbruzzo.length;

      const elBoll1 = document.getElementById("bollettino-testo-1");
      const elBoll2 = document.getElementById("bollettino-testo-2");

      if (elBoll1 && elBoll2) {
        const meteoMonti = descriviSituazione(dati[8].current.weather_code);
        const meteoCosta = descriviSituazione(dati[1].current.weather_code);
        const tempRoccaraso = dati[8].current.temperature_2m;
        const tempPescara = dati[1].current.temperature_2m;
        const umidita = dati[8].current.relative_humidity_2m;
        const ventoMedio = Math.round(sommaVento / dati.length);

        elBoll1.innerHTML = `In questo momento sull'Abruzzo si rileva <strong>${meteoMonti}</strong> sui settori interni e montani (Roccaraso <strong>${tempRoccaraso}°C</strong>, umidità ${umidita}%) e <strong>${meteoCosta}</strong> lungo la fascia costiera adriatica (Pescara <strong>${tempPescara}°C</strong>).`;
        elBoll2.innerHTML = `Ventilazione media regionale intorno a <strong>${ventoMedio} km/h</strong>, con escursione termica attuale compresa tra i <strong>${minTemp}°C</strong> di ${nomeFredda} e i <strong>${maxTemp}°C</strong> di ${nomeCalda}.`;
      }

    } catch (errore) {
      console.error("Errore aggiornamento meteo Abruzzo:", errore);
    }
  }

  aggiornaTuttoInTempoReale();
  setInterval(aggiornaTuttoInTempoReale, 900000);
});
