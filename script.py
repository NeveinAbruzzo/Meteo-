function cambiaScheda(nome, btn) {
    document.querySelectorAll('.sezione').forEach(s => s.classList.remove('attiva'));
    document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
    document.getElementById('sez-' + nome).classList.add('attiva');
    btn.classList.add('active');
}

async function aggiornaDatiMeteo() {
    try {
        const risposta = await fetch('dati-meteo.txt?t=' + new Date().getTime());
        if (!risposta.ok) throw new Error('Impossibile leggere dati-meteo.txt');
        
        const testo = await risposta.text();
        const righe = testo.trim().split('\n');
        const dati = [];

        righe.forEach(riga => {
            if (!riga.trim()) return;
            const match = riga.match(/^([^:]+):\s*(-?\d+(?:[.,]\d+)?)/);
            if (match) {
                const localita = match.trim();
                const temp = parseFloat(match.replace(',', '.'));
                if (!isNaN(temp)) {
                    dati.push({ localita, temp });
                }
            }
        });

        if (dati.length === 0) return;

        const tickerBox = document.getElementById('ticker-box');
        const tabellaBody = document.getElementById('tabella-body');
        
        tickerBox.innerHTML = '';
        tabellaBody.innerHTML = '';

        let max = dati;
        let min = dati;

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
        document.getElementById('ultimo-aggiornamento').textContent = `Aggiornato automaticamente il ${ora}`;

    } catch (errore) {
        console.error('Errore:', errore);
        document.getElementById('ultimo-aggiornamento').textContent = 'Errore nel caricamento di dati-meteo.txt';
    }
}

aggiornaDatiMeteo();
setInterval(aggiornaDatiMeteo, 60000);
