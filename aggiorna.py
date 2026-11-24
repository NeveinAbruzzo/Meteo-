import time
import requests
from datetime import datetime
from zoneinfo import ZoneInfo

localita = [
    {"nome": "L'Aquila", "lat": 42.3498, "lon": 13.3995},
    {"nome": "Pescara", "lat": 42.4618, "lon": 14.2161},
    {"nome": "Chieti", "lat": 42.3483, "lon": 14.1649},
    {"nome": "Teramo", "lat": 42.6589, "lon": 13.7044},
    {"nome": "Roccaraso", "lat": 41.8487, "lon": 14.0785},
    {"nome": "Pescocostanzo", "lat": 41.8872, "lon": 14.0661},
    {"nome": "Scanno", "lat": 41.9044, "lon": 13.8796},
    {"nome": "Villetta Barrea", "lat": 41.7554, "lon": 13.9909},
    {"nome": "Campo Imperatore", "lat": 42.4431, "lon": 13.5586},
    {"nome": "Ovindoli", "lat": 42.1384, "lon": 13.5161},
    {"nome": "Campo Felice", "lat": 42.2217, "lon": 13.4561},
    {"nome": "Avezzano", "lat": 42.0312, "lon": 13.4262},
    {"nome": "Sulmona", "lat": 42.0493, "lon": 13.9258},
    {"nome": "Lanciano", "lat": 42.2271, "lon": 14.3905},
    {"nome": "Vasto", "lat": 42.1118, "lon": 14.7061}
]

headers = {
    "User-Agent": "Mozilla/5.0 (compatible; NeveInAbruzzoBot/1.0)",
    "Accept": "application/json"
}

risultati = []
for p in localita:
    url = f"https://open-meteo.com{p['lat']}&longitude={p['lon']}&current=temperature_2m"
    try:
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
        r = resp.json()
        temp = float(r["current"]["temperature_2m"])
        print(f"OK {p['nome']}: {temp}°C")
    except Exception as e:
        print(f"ERRORE {p['nome']}: {e}")
        temp = 5.0
    risultati.append({"nome": p["nome"], "temp": temp})
    time.sleep(0.4)

piu_calda = max(risultati, key=lambda x: x["temp"])
piu_fredda = min(risultati, key=lambda x: x["temp"])
ora = datetime.now(ZoneInfo("Europe/Rome")).strftime("%d/%m/%Y %H:%M")

ticker_html = "".join([f'<div class="ticker-item">{x["nome"]}: <span>{x["temp"]}°C</span></div>' for x in risultati])
tabella_html = "".join([f'<tr><td>{x["nome"]}</td><td class="temp-col">{x["temp"]}°C</td></tr>' for x in risultati])

html = f"""<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Meteo Abruzzo Live</title>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }}
        body {{ background-color: #f0f4f8; color: #333; display: flex; flex-direction: column; min-height: 100vh; font-size: 14px; }}
        .ticker-wrap {{ width: 100%; overflow: hidden; background-color: #004472; color: white; padding: 6px 0; white-space: nowrap; }}
        .ticker {{ display: inline-block; padding-left: 100%; animation: scorrimento 35s linear infinite; }}
        .ticker-item {{ display: inline-block; padding: 0 20px; font-size: 0.85rem; }}
        .ticker-item span {{ font-weight: bold; color: #ffdd57; margin-left: 4px; }}
        @keyframes scorrimento {{ 0% {{ transform: translate3d(0, 0, 0); }} 100% {{ transform: translate3d(-100%, 0, 0); }} }}
        nav {{ background-color: #005b96; padding: 8px 15px; display: flex; justify-content: center; gap: 10px; }}
        .nav-btn {{ background-color: rgba(255, 255, 255, 0.15); color: white; border: 1px solid rgba(255, 255, 255, 0.3); padding: 5px 14px; border-radius: 4px; font-size: 0.85rem; cursor: pointer; }}
        .nav-btn.active {{ background-color: #ffdd57; color: #003356; font-weight: bold; }}
        .sezione {{ display: none; flex: 1; flex-direction: column; align-items: center; padding: 25px 15px; max-width: 750px; margin: 0 auto; width: 100%; }}
        .sezione.attiva {{ display: flex; }}
        #sez-home {{ justify-content: center; }}
        .period-title {{ font-size: 1.15rem; margin-bottom: 18px; color: #102a43; text-align: center; text-transform: uppercase; }}
        .records-container {{ display: flex; gap: 15px; width: 100%; justify-content: center; flex-wrap: wrap; }}
        .record-card {{ background: white; border-radius: 8px; padding: 18px 15px; width: 230px; text-align: center; box-shadow: 0 4px 12px rgba(0,0,0,0.06); }}
        .card-max {{ border-top: 4px solid #e63946; }}
        .card-min {{ border-top: 4px solid #00a8e8; }}
        .record-label {{ font-size: 0.75rem; text-transform: uppercase; font-weight: bold; color: #627d98; margin-bottom: 6px; }}
        .record-value {{ font-size: 2.1rem; font-weight: 800; margin-bottom: 5px; }}
        .card-max .record-value {{ color: #e63946; }}
        .card-min .record-value {{ color: #00a8e8; }}
        .webcam-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 12px; width: 100%; }}
        .cam-btn {{ background: white; border: 1px solid #d9e2ec; border-left: 4px solid #005b96; border-radius: 6px; padding: 14px 16px; text-decoration: none; color: #102a43; display: flex; flex-direction: column; gap: 4px; }}
        .cam-station {{ font-weight: bold; font-size: 0.95rem; color: #005b96; }}
        .cam-altitude {{ font-size: 0.78rem; color: #627d98; }}
        .meteo-table {{ width: 100%; max-width: 450px; background: white; border-radius: 8px; border-collapse: collapse; }}
        .meteo-table th, .meteo-table td {{ padding: 10px 15px; text-align: left; border-bottom: 1px solid #e2e8f0; }}
        .meteo-table th {{ background-color: #005b96; color: white; }}
        .temp-col {{ font-weight: bold; color: #004472; text-align: right; }}
        .status-msg {{ margin-top: 15px; font-size: 0.8rem; color: #627d98; }}
    </style>
</head>
<body>
    <div class="ticker-wrap"><div class="ticker">{ticker_html}</div></div>
    <nav>
        <button class="nav-btn active" onclick="cambiaScheda('home', this)">Home Page</button>
        <button class="nav-btn" onclick="cambiaScheda('webcam', this)">Dati Meteo &amp; Webcam</button>
        <button class="nav-btn" onclick="cambiaScheda('tabella', this)">Temperature Abruzzo</button>
    </nav>
    <main id="sez-home" class="sezione attiva">
        <h1 class="period-title">Estremi Termici Attuali Abruzzo</h1>
        <div class="records-container">
            <div class="record-card card-max">
                <div class="record-label">Temperatura più alta</div>
                <div class="record-value">{piu_calda['temp']}°C</div>
                <div class="record-details">{piu_calda['nome']}</div>
            </div>
            <div class="record-card card-min">
                <div class="record-label">Temperatura più bassa</div>
                <div class="record-value">{piu_fredda['temp']}°C</div>
                <div class="record-details">{piu_fredda['nome']}</div>
            </div>
        </div>
        <div class="status-msg">Aggiornato automaticamente il {ora}</div>
    </main>
    <section id="sez-webcam" class="sezione">
        <h1 class="period-title">Webcam Live Stazioni Sciistiche</h1>
        <div class="webcam-grid">
            <a href="https://roccaraso.net" target="_blank" class="cam-btn"><span class="cam-station">Roccaraso - Alto Sangro</span><span class="cam-altitude">Aremogna • Pizzalto • Monte Pratello</span></a>
            <a href="https://campofelice.it" target="_blank" class="cam-btn"><span class="cam-station">Campo Felice</span><span class="cam-altitude">Brecciara • Cerchiare • Panoramica 360°</span></a>
            <a href="https://ovindolimagnola.it" target="_blank" class="cam-btn"><span class="cam-station">Ovindoli - Monte Magnola</span><span class="cam-altitude">Dolce Vita • Anfiteatro • Monte Freddo</span></a>
            <a href="https://skiresort.it" target="_blank" class="cam-btn"><span class="cam-station">Campo Imperatore</span><span class="cam-altitude">Gran Sasso • Scindarella • Funivia</span></a>
            <a href="https://dovesciare.it" target="_blank" class="cam-btn"><span class="cam-station">Passolanciano - Majelletta</span><span class="cam-altitude">Majella • Rifugio Pomilio 1890m</span></a>
            <a href="https://meteoregioneabruzzo.it" target="_blank" class="cam-btn"><span class="cam-station">Pescasseroli</span><span class="cam-altitude">Impianti Sci • Monte delle Vitelle</span></a>
            <a href="https://skiinfo.it" target="_blank" class="cam-btn"><span class="cam-station">Tutte le Stazioni Abruzzo</span><span class="cam-altitude">Riepilogo piste e neve in diretta</span></a>
        </div>
    </section>
    <section id="sez-tabella" class="sezione">
        <h1 class="period-title">Temperature Live Località Abruzzo</h1>
        <table class="meteo-table">
            <thead><tr><th>Località</th><th style="text-align: right;">Temperatura</th></tr></thead>
            <tbody>{tabella_html}</tbody>
        </table>
    </section>
    <script>
        function cambiaScheda(nome, btn) {{
            document.querySelectorAll('.sezione').forEach(s => s.classList.remove('attiva'));
            document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
            document.getElementById('sez-' + nome).classList.add('attiva');
            btn.classList.add('active');
        }}
    </script>
</body>
</html>"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
