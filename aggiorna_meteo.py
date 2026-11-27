import urllib.request
import json
import subprocess
import time
from datetime import datetime

citta = [
    ("L'Aquila", 42.35, 13.40), ("Pescara", 42.46, 14.21), ("Chieti", 42.35, 14.17),
    ("Teramo", 42.66, 13.70), ("Roccaraso", 41.85, 14.08), ("Pescocostanzo", 41.89, 14.07),
    ("Scanno", 41.90, 13.88), ("Villetta Barrea", 41.78, 13.94), ("Campo Imperatore", 42.44, 13.56),
    ("Ovindoli", 42.14, 13.52), ("Campo Felice", 42.22, 13.43), ("Avezzano", 42.03, 13.43),
    ("Sulmona", 42.05, 13.93), ("Lanciano", 42.23, 14.39), ("Vasto", 42.11, 14.71)
]

while True:
    try:
        out = []
        for nome, lat, lon in citta:
            url = f"https://open-meteo.com{lat}&longitude={lon}&current=temperature_2m"
            data = json.loads(urllib.request.urlopen(url, timeout=10).read().decode())
            out.append({"nome": nome, "temp": data["current"]["temperature_2m"]})

        ora = datetime.now().strftime("%d/%m/%Y %H:%M")
        with open("dati.json", "w", encoding="utf-8") as f:
            json.dump({"ora": ora, "dati": out}, f, ensure_ascii=False)

        subprocess.run(["git", "add", "dati.json"])
        subprocess.run(["git", "commit", "-m", f"Meteo {ora}"])
        subprocess.run(["git", "push"])
        print(f"[{ora}] Aggiornato su GitHub con successo!")
    except Exception as e:
        print("Errore:", e)

    time.sleep(600)  # Ripete ogni 10 minuti

