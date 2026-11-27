import urllib.request
import json
import base64
import time
from datetime import datetime

TOKEN = "INCOLLA_QUI_IL_TUO_TOKEN_GITHUB"
REPO = "NeveinAbruzzo/Meteo-"
FILE = "dati.json"

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
        testo = json.dumps({"ora": ora, "dati": out}, ensure_ascii=False)
        b64 = base64.b64encode(testo.encode("utf-8")).decode("utf-8")

        api = f"https://github.com{REPO}/contents/{FILE}"
        headers = {"Authorization": f"token {TOKEN}", "Accept": "application/vnd.github.v3+json"}

        sha = None
        try:
            info = json.loads(urllib.request.urlopen(urllib.request.Request(api, headers=headers)).read().decode())
            sha = info["sha"]
        except Exception:
            pass

        payload = {"message": f"Meteo {ora}", "content": b64}
        if sha:
            payload["sha"] = sha

        req = urllib.request.Request(api, data=json.dumps(payload).encode("utf-8"), headers=headers, method="PUT")
        urllib.request.urlopen(req)
        print(f"[{ora}] Temperature reali pubblicate su GitHub!")
    except Exception as e:
        print("Errore:", e)

    time.sleep(600)
