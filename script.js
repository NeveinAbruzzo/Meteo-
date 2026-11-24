document.getElementById('last-update').textContent = 'Script avviato! Scarico i dati...';

function cambiaScheda(nome, btn) {
    var sezioni = document.querySelectorAll('.sezione');
    for (var i = 0; i < sezioni.length; i++) {
        sezioni[i].classList.remove('attiva');
    }
    var bottoni = document.querySelectorAll('.nav-btn');
    for (var j = 0; j < bottoni.length; j++) {
        bottoni[j].classList.remove('active');
    }
    document.getElementById('sez-' + nome).classList.add('attiva');
    btn.classList.add('active');
}

var localita = [
    { nome: "L'Aquila", lat: 42.3498, lon: 13.3995 },
    { nome: "Pescara", lat: 42.4618, lon: 14.2161 },
    { nome: "Chieti", lat: 42.3510, lon: 14.1675 },
    { nome: "Teramo", lat: 42.6589, lon: 13.7044 },
    { nome: "Roccaraso", lat: 41.8465, lon: 14.0792 },
    { nome: "Pescocostanzo", lat: 41.8894, lon: 14.0653 },
    { nome: "Scanno", lat: 41.9026, lon: 13.8803 },
    { nome: "Villetta Barrea", lat: 41.7766, lon: 13.9392 },
    { nome: "Campo Imperatore", lat: 42.4431, lon: 13.5592 },
    { nome: "Ovindoli", lat: 42.1375, lon: 13.5169 },
    { nome: "Campo Felice", lat: 42.2158, lon: 13.4561 },
    { nome: "Avezzano", lat: 42.0312, lon: 13.4263 },
    { nome: "Sulmona", lat: 42.0494, lon: 13.9255 },
    { nome: "Lanciano", lat: 42.2266, lon: 14.3905 },
    { nome: "Vasto", lat: 42.1122, lon: 14.7081 }
];

function aggiornaMeteo() {
    var statusEl = document.getElementById('last-update');
    var lats = [];
    var lons = [];
    
    for (var i = 0; i < localita.length; i++) {
        lats.push(localita[i].lat);
        lons.push(localita[i].lon);
    }

    var url = "https://open-meteo.com" + lats.join(",") + "&longitude=" + lons.join(",") + "&current=temperature_2m";

    fetch(url)
        .then(function(response) {
            if (!response.ok) {
                throw new Error("HTTP " + response.status);
            }
            return response.json();
        })
        .then(function(dati) {
            var listaDati = Array.isArray(dati) ? dati : [dati];
            var tickerHTML = "";
            var tabellaHTML = "";
            var maxTemp = -999, maxCity = "";
            var minTemp = 999, minCity = "";

            for (var i = 0; i < listaDati.length; i++) {
                var nome = localita[i].nome;
                var temp = listaDati[i].current.temperature_2m;
                var tempStr = temp.toFixed(1) + "°C";

                if (temp > maxTemp) { maxTemp = temp; maxCity = nome; }
                if (temp < minTemp) { minTemp = temp; minCity = nome; }

                tickerHTML += '<div class="ticker-item">' + nome + ': <span>' + tempStr + '</span></div>';
                tabellaHTML += '<tr><td>' + nome + '</td><td class="temp-col">' + tempStr + '</td></tr>';
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

aggiornaMeteo();
setInterval(aggiornaMeteo, 900000);
