function cambiaScheda(nome, btn) {
    document.querySelectorAll('.sezione').forEach(s => s.classList.remove('attiva'));
    document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
    document.getElementById('sez-' + nome).classList.add('attiva');
    btn.classList.add('active');
}

const localita = [
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

async function aggiornaMeteo() {
    const lats = localita.map(l => l.lat).join(',');
    const lons = localita.map(l => l.lon).join(',');
    const url = `https://open-meteo.com{lats}&longitude=${lons}&current=temperature_2m&timezone=Europe%2FRome`;

    try {
        const response = await fetch(url);
        const dati = await response.json();

        let tickerHTML = '';
        let tabellaHTML = '';
        let maxTemp = -Infinity, maxCity = '';
        let minTemp = Infinity, minCity = '';

        dati.forEach((item, index) => {
            const nome = localita[index].nome;
            const temp = item.current.temperature_2m;
            const tempStr = temp.toFixed(1) + '°C';

            if (temp > maxTemp) { maxTemp = temp; maxCity = nome; }
            if (temp < minTemp) { minTemp = temp; minCity = nome; }

            tickerHTML += `<div class="ticker-item">${nome}: <span>${tempStr}</span></div>`;
            tabellaHTML += `<tr><td>${nome}</td><td class="temp-col">${tempStr}</td></tr>`;
        });

        document.getElementById('ticker-list').innerHTML = tickerHTML;
        document.getElementById('tabella-body').innerHTML = tabellaHTML;
        document.getElementById('max-temp').textContent = maxTemp.toFixed(1) + '°C';
        document.getElementById('max-city').textContent = maxCity;
        document.getElementById('min-temp').textContent = minTemp.toFixed(1) + '°C';
        document.getElementById('min-city').textContent = minCity;

        const ora = new Date();
        const dataFormattata = ora.toLocaleDateString('it-IT') + ' ' + ora.toLocaleTimeString('it-IT', { hour: '2-digit', minute: '2-digit' });
        document.getElementById('last-update').textContent = 'Aggiornato automaticamente il ' + dataFormattata;

    } catch (errore) {
        document.getElementById('last-update').textContent = 'Errore nel caricamento dei dati meteo. Riprova più tardi.';
        console.error(errore);
    }
}

aggiornaMeteo();
setInterval(aggiornaMeteo, 900000);
