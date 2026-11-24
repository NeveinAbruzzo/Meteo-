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

var localitaAbruzzo = [
    "l'aquila", "pescara", "chieti", "teramo", "roccaraso",
    "pescocostanzo", "scanno", "villetta barrea", "campo imperatore",
    "ovindoli", "campo felice", "avezzano", "sulmona", "lanciano", "vasto"
];

function aggiornaDaFile() {
    var statusEl = document.getElementById('last-update');
    statusEl.textContent = "Lettura di Dati_meteo.txt in corso...";
    
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

            for (var i = 0; i < righe.length; i++) {
                var riga = righe[i].trim();
                if (riga === "" || riga.indexOf(':') === -1) continue;

                var parti = riga.split(':');
                var nome = parti[0].trim();
                var tempTesto = parti[1].trim();

                if (localitaAbruzzo.indexOf(nome.toLowerCase()) !== -1) {
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

aggiornaDaFile();
setInterval(aggiornaDaFile, 300000);
