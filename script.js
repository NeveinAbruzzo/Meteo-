function cambiaScheda(nome, btn) {
    var sezioni = document.querySelectorAll('.sezione');
    sezioni.forEach(function(s) {
        s.classList.remove('attiva');
    });
    var bottoni = document.querySelectorAll('.nav-btn');
    bottoni.forEach(function(b) {
        b.classList.remove('active');
    });
    document.getElementById('sez-' + nome).classList.add('attiva');
    btn.classList.add('active');
}

var elencoAbruzzo = "|l'aquila|pescara|chieti|teramo|roccaraso|pescocostanzo|scanno|villetta barrea|campo imperatore|ovindoli|campo felice|avezzano|sulmona|lanciano|vasto|";

function aggiornaDaFile() {
    var statusEl = document.getElementById('last-update');
    var url = "Dati_meteo.txt?t=" + new Date().getTime();

    fetch(url)
        .then(function(response) {
            if (!response.ok) {
                throw new Error("File Dati_meteo.txt non trovato (Codice " + response.status + ")");
            }
            return response.text();
        })
        .then(function(testo) {
            var righe = testo.split('\n');
            var tickerHTML = "";
            var tabellaHTML = "";
            var maxTemp = -999, maxCity = "";
            var minTemp = 999, minCity = "";
            var trovate = 0;

            righe.forEach(function(rigaRaw) {
                var riga = rigaRaw.trim();
                var posDuePunti = riga.indexOf(':');
                
                if (riga !== "" && posDuePunti !== -1) {
                    var nome = riga.substring(0, posDuePunti).trim();
                    var tempTesto = riga.substring(posDuePunti + 1).trim();

                    if (elencoAbruzzo.indexOf("|" + nome.toLowerCase() + "|") !== -1) {
                        var numeroTemp = parseFloat(tempTesto.replace('°C', '').replace(',', '.'));

                        if (!isNaN(numeroTemp)) {
                            trovate++;
                            var tempFormattata = numeroTemp.toFixed(1) + "°C";

                            if (numeroTemp > maxTemp) { maxTemp = numeroTemp; maxCity = nome; }
                            if (numeroTemp < minTemp) { minTemp = numeroTemp; minCity = nome; }

                            tickerHTML += '<div class="ticker-item">' + nome + ': <span>' + tempFormattata + '</span></div>';
                            tabellaHTML += '<tr><td>' + nome + '</td><td class="temp-col">' + tempFormattata + '</td></tr>';
                        }
                    }
                }
            });

            if (trovate === 0) {
                throw new Error("Nessuna località abruzzese trovata in Dati_meteo.txt");
            }

            document.getElementById('ticker-list').innerHTML = tickerHTML;
            document.getElementById('tabella-body').innerHTML = tabellaHTML;
            document.getElementById('max-temp').textContent = maxTemp.toFixed(1) + "°C";
            document.getElementById('max-city').textContent = maxCity;
            document.getElementById('min-temp').textContent = minTemp.toFixed(1) + "°C";
            document.getElementById('min-city').textContent = minCity;

            var ora = new Date();
            var minuti = ora.getMinutes() < 10 ? "0" + ora.getMinutes() : ora.getMinutes();
            statusEl.textContent = "Aggiornato alle " + ora.getHours() + ":" + minuti;
            statusEl.style.color = "#627d98";
        })
        .catch(function(errore) {
            statusEl.textContent = "Errore: " + errore.message;
            statusEl.style.color = "red";
        });
}

function interpretaMeteo(codice) {
    if (codice === 0) return { icona: "☀️", testo: "Sereno" };
    if (codice <= 3) return { icona: "⛅", testo: "Poco nuvoloso" };
    if (codice <= 48) return { icona: "🌫️", testo: "Nebbia" };
    if (codice <= 67) return { icona: "🌧️", testo: "Pioggia" };
    if (codice <= 77) return { icona: "❄️", testo: "Neve" };
    if (codice <= 82) return { icona: "🌦️", testo: "Rovesci" };
    if (codice <= 86) return { icona: "🌨️", testo: "Neve forte" };
    return { icona: "⛈️", testo: "Temporali" };
}

function aggiornaPrevisioni() {
    var boxPrevisioni = document.getElementById('forecast-days');
    var urlPrev = "https://open-meteo.com";

    fetch(urlPrev)
        .then(function(r) {
            if (!r.ok) throw new Error("HTTP " + r.status);
            return r.json();
        })
        .then(function(dati) {
            var giorni = dati.daily.time;
            var codici = dati.daily.weathercode;
            var maxList = dati.daily.temperature_2m_max;
            var minList = dati.daily.temperature_2m_min;
            var html = "";

            for (var i = 1; i <= 3; i++) {
                var dataStr = giorni.slice(i, i + 1).shift();
                var codice = codici.slice(i, i + 1).shift();
                var tMax = maxList.slice(i, i + 1).shift();
                var tMin = minList.slice(i, i + 1).shift();

                var partiData = dataStr.split('-');
                var dataObj = new Date(partiData.slice(0,1).shift(), partiData.slice(1,2).shift() - 1, partiData.slice(2,3).shift());
                var nomeGiorno = dataObj.toLocaleDateString('it-IT', { weekday: 'short', day: 'numeric', month: 'short' });
                var info = interpretaMeteo(codice);

                html += '<div class="forecast-day">';
                html += '<div class="f-day-name">' + nomeGiorno + '</div>';
                html += '<div class="f-icon">' + info.icona + '</div>';
                html += '<div class="f-desc">' + info.testo + '</div>';
                html += '<div class="f-temps"><span class="f-min">' + Math.round(tMin) + '°</span> / <span class="f-max">' + Math.round(tMax) + '°</span></div>';
                html += '</div>';
            }

            boxPrevisioni.innerHTML = html;
        })
        .catch(function() {
            // Se il server blocca la chiamata esterna, mostra le schede con link diretti alle previsioni
            var oggi = new Date();
            var htmlFallback = "";
            for (var i = 1; i <= 3; i++) {
                var d = new Date(oggi.getTime() + (i * 86400000));
                var nomeG = d.toLocaleDateString('it-IT', { weekday: 'short', day: 'numeric', month: 'short' });
                htmlFallback += '<a href="https://ilmeteo.it" target="_blank" class="forecast-day" style="text-decoration:none;">';
                htmlFallback += '<div class="f-day-name">' + nomeG + '</div>';
                htmlFallback += '<div class="f-icon">🌤️</div>';
                htmlFallback += '<div class="f-desc" style="color:#005b96; font-weight:bold;">Vedi bollettino →</div>';
                htmlFallback += '</a>';
            }
            boxPrevisioni.innerHTML = htmlFallback;
        });
}

aggiornaDaFile();
aggiornaPrevisioni();
setInterval(aggiornaDaFile, 300000);
