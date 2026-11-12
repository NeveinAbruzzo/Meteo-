from datetime import datetime
from zoneinfo import ZoneInfo
import os
import time
import requests


def ottieni_temperatura_singola(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; NeveInAbruzzoBot/1.0)",
        "Accept": "application/json"
    }
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        dati = response.json()
        return f"{dati['current']['temperature_2m']}°C"
    except Exception as e:
        print(f"Errore chiamata ({url[:45]}...): {e}")
        return None


def salva_meteo_comprensorio():
    orario_locale = datetime.now(ZoneInfo("Europe/Rome")).strftime("%d/%m/%Y %H:%M")

    # Inserisci o modifica qui i link diretti presi da Open-Meteo per ogni città
    localita = [
        {
            "nome": "Roccaraso",
            "url": "https://api.open-meteo.com/v1/forecast?latitude=41.8487&longitude=14.0785&current=temperature_2m",
            "fallback": "6.2°C"
        },
        {
            "nome": "Scanno",
            "url": "https://api.open-meteo.com/v1/forecast?latitude=41.9044&longitude=13.8796&current=temperature_2m",
            "fallback": "6.5°C"
        },
        {
            "nome": "Frosinone",
            "url": "https://api.open-meteo.com/v1/forecast?latitude=41.6398&longitude=13.3411&current=temperature_2m",
            "fallback": "11.5°C"
        },
        {
            "nome": "Pescocostanzo",
            "url": "https://api.open-meteo.com/v1/forecast?latitude=41.8872&longitude=14.0661&current=temperature_2m",
            "fallback": "5.8°C"
        },
        {
            "nome": "Villetta Barrea",
            "url": "https://api.open-meteo.com/v1/forecast?latitude=41.7554&longitude=13.9909&current=temperature_2m",
            "fallback": "7.0°C"
        },
        {
            "nome": "Chieti",
            "url": "https://api.open-meteo.com/v1/forecast?latitude=42.3483&longitude=14.1649&current=temperature_2m",
            "fallback": "12.0°C"
        },
        {
            "nome": "Napoli",
            "url": "https://api.open-meteo.com/v1/forecast?latitude=40.8762&longitude=14.5195&current=temperature_2m",
            "fallback": "14.8°C"
        },
    ]

    righe_da_salvare = []

    print("--- AVVIO RECUPERO DATI METEO COMPRENSORIO ---")
    righe_da_salvare.append(f"=== ULTIMO AGGIORNAMENTO: {orario_locale} ===\n\n")

    for posto in localita:
        temperatura_attuale = ottieni_temperatura_singola(posto["url"])

        if temperatura_attuale is not None:
            print(f"Dato reale per {posto['nome']}: {temperatura_attuale}")
        else:
            temperatura_attuale = posto["fallback"]
            print(f"ATTENZIONE: Uso fallback per {posto['nome']}: {temperatura_attuale}")

        righe_da_salvare.append(f"{posto['nome']}: {temperatura_attuale}\n")
        
        # Piccola pausa di sicurezza per non sovraccaricare l'API tra una città e l'altra
        time.sleep(0.3)

    try:
        cartella = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(cartella, "Dati_meteo.txt")
        with open(file_path, "w", encoding="utf-8") as file:
            file.writelines(righe_da_salvare)
        print("--- SOVRASCRITTURA TXT LOCALE COMPLETATA ---")
    except Exception as file_error:
        print(f"Errore scrittura file: {file_error}")


if __name__ == "__main__":
    salva_meteo_comprensorio()



document.addEventListener("DOMContentLoaded", function () {
  // 1. Stile CSS della barra scorrevole
  const stile = document.createElement("style");
  stile.textContent = `
    .ticker-meteo-container {
      width: 100%;
      background-color: #1565c0;
      color: #ffffff;
      font-family: Arial, sans-serif;
      font-size: 15px;
      display: flex;
      align-items: center;
      overflow: hidden;
      height: 38px;
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

  // 2. Creazione barra e posizionamento
  const barra = document.createElement("div");
  barra.className = "ticker-meteo-container";
  barra.innerHTML = `
    <div class="ticker-meteo-label">TEMPERATURE LIVE:</div>
    <div class="ticker-meteo-scroll" id="testo-temperature-live">Caricamento dati live...</div>
  `;

  // Inserisce la barra dopo il menu (cambia '.menu-nav' con la classe del tuo menu nero se necessario)
  const menu = document.querySelector("nav, .navbar, .menu");
  if (menu) {
    menu.insertAdjacentElement("afterend", barra);
  } else {
    document.body.prepend(barra);
  }

  // 3. Stazioni del comprensorio
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
    if (code === 0) return "un quadro stabile con cielo prevalentemente sereno";
    if (code >= 1 && code <= 3) return "un quadro variabile con transito di nuvolosità medio-alta e schiarite";
    if (code === 45 || code === 48) return "condizioni di stabilità con foschie o locali banchi di nebbia nelle valli";
    if (code >= 51 && code <= 67) return "condizioni di instabilità con precipitazioni sparse sul comprensorio";
    if (code >= 71 && code <= 77) return "precipitazioni a carattere nevoso sulle zone montane e appenniniche";
    if (code >= 80 && code <= 82) return "rovesci sparsi alternati a temporanee schiarite";
    if (code >= 95) return "spiccata instabilità atmosferica con possibili fenomeni temporaleschi";
    return "nuvolosità irregolare su gran parte del territorio";
  }

  async function aggiornaTuttoInTempoReale() {
    try {
      const lats = localita.map(c => c.lat).join(",");
      const lons = localita.map(c => c.lon).join(",");
      const url = `https://open-meteo.com{lats}&longitude=${lons}&current=temperature_2m,weather_code,wind_speed_10m&timezone=Europe%2FRome`;

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

        return `${nome}: ${temp}°C ${ottieniIcona(code)}`;
      });

      // A. Aggiorna la barra scorrevole
      document.getElementById("testo-temperature-live").innerHTML =
        stringheBarra.join(" &nbsp;&nbsp;&nbsp;•&nbsp;&nbsp;&nbsp; ");

      // B. Aggiorna l'orario sotto "Meteo Portale"
      const elOrario = document.getElementById("ultimo-aggiornamento");
      if (elOrario) {
        const adesso = new Date().toLocaleString("it-IT", {
          day: "2-digit", month: "2-digit", year: "numeric",
          hour: "2-digit", minute: "2-digit"
        });
        elOrario.textContent = `--- ULTIMO AGGIORNAMENTO: ${adesso} ---`;
      }

      // C. Aggiorna "Estremi Rilevati" nella colonna di destra
      const elCalda = document.getElementById("estremo-caldo");
      const elFredda = document.getElementById("estremo-freddo");
      const elStazioni = document.getElementById("stazioni-attive");

      if (elCalda) elCalda.textContent = cittaCalda;
      if (elFredda) elFredda.textContent = cittaFredda;
      if (elStazioni) elStazioni.textContent = localita.length;

      // D. Aggiorna il "Bollettino Meteorologico Generale" (usa Roccaraso come riferimento Abruzzo)
      const elBoll1 = document.getElementById("bollettino-testo-1");
      const elBoll2 = document.getElementById("bollettino-testo-2");

      if (elBoll1 && elBoll2) {
        const codiceAbruzzo = dati[0].current.weather_code; // Roccaraso
        const ventoMedio = Math.round(sommaVento / dati.length);
        const tipoVento = ventoMedio < 15 ? "debole" : (ventoMedio < 30 ? "moderata" : "forte");

        elBoll1.textContent = `La situazione attuale sul territorio abruzzese e sul comprensorio mostra ${descriviSituazione(codiceAbruzzo)}. ` +
                              `Nel corso della giornata si rileva una ventilazione ${tipoVento} (media ${ventoMedio} km/h), con valori termici compresi tra ${minTemp}°C e ${maxTemp}°C.`;
        
        elBoll2.textContent = `Dati aggiornati in tempo reale dalla rete di monitoraggio (${localita.length} stazioni attive).`;
      }

    } catch (errore) {
      console.error("Errore aggiornamento meteo:", errore);
    }
  }

  // Avvia al caricamento e aggiorna ogni 15 minuti
  aggiornaTuttoInTempoReale();
  setInterval(aggiornaTuttoInTempoReale, 900000);
});
