function cambiaScheda(nome, btn) {
    document.querySelectorAll('.sezione').forEach(s => s.classList.remove('attiva'));
    document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
    document.getElementById('sez-' + nome).classList.add('attiva');
    btn.classList.add('active');
}

function mostraDatiInPagina(testo, fonte) {
    const righe = testo.trim().split('\n');
    const dati = [];

    righe.forEach(riga => {
        if (!riga.includes(':')) return;
        const parti = riga.split(':');
        const localita = parti.at(0).trim();
        const numeroPulito = parti.at(1).replace('°C', '').replace(',', '.').trim();
        const temp = parseFloat(numeroPulito);

        if (localita && !isNaN(temp)) {
            dati.push({ localita, temp });
        }
    });

    if (dati.length === 0) return;

    const tickerBox = document.getElementById('ticker-box');
    const tabellaBody = document.getElementById('tabella-body');

    tickerBox.innerHTML = '';
    tabellaBody.innerHTML = '';

    let max = dati.at(0);
    let min = dati.at(0);

    dati.forEach(item => {
        const tempFormattata = item.temp.toFixed(1) + '°C';

        tickerBox.innerHTML += `<div class="ticker-item">${item.localita}: <span>${tempFormattata}</span></div>`;
        tabellaBody.innerHTML += `<tr><td>${item.localita}</td><td class="temp-col">${tempFormattata}</td></tr>`;

        if (item.temp > max.temp) max = item;
        if (item.temp < min.temp) min = item;
    });

    document.getElementById('max-temp').textContent = max.temp.toFixed(1) + '°C';
    document.getElementById('max-loc').textContent = max.localita;

    document.getElementById('min-temp').textContent = min.temp.toFixed(1) + '°C';
    document.getElementById('min-loc').textContent = min.localita;

    const ora = new Date().toLocaleString('it-IT', { dateStyle: 'short', timeStyle: 'short' });
    document.getElementById('ultimo-aggiornamento').textContent = `Aggiornato il ${ora} (${fonte})`;
}

async function aggiornaDatiMeteo() {
    try {
        const risposta = await fetch('Dati_meteo.txt?t=' + Date.now());
        if (!risposta.ok) throw new Error('File non trovato');
        const testo = await risposta.text();
        mostraDatiInPagina(testo, 'da dati-meteo.txt');
    } catch (errore) {
        // Se apri il file con doppio clic sul PC, il browser blocca fetch(): uso i dati di riserva
        const datiRiserva = `
Roccaraso: 6.1°C
Scanno: 8.2°C
Frosinone: 13.4°C
Pescocostanzo: 6.0°C
Villetta Barrea: 7.5°C
Chieti: 10.8°C
Napoli: 15.8°C`;
        mostraDatiInPagina(datiRiserva, 'modalità locale PC - carica su server per lettura live');
    }
}

aggiornaDatiMeteo();
setInterval(aggiornaDatiMeteo, 60000);
