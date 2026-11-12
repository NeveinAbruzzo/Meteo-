from datetime import datetime
from zoneinfo import ZoneInfo
import os
import time
import requests


def ottieni_temperature_comprensorio(localita):
    latitudini = ",".join(str(posto["lat"]) for posto in localita)
    longitudini = ",".join(str(posto["lon"]) for posto in localita)

    url = (
        f"https://open-meteo.com"
        f"?latitude={latitudini}&longitude={longitudini}"
        f"&current=temperature_2m&timezone=Europe%2FRome"
    )

    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; NeveInAbruzzoBot/1.0)",
        "Accept": "application/json"
    }

    # Prova fino a 3 volte in caso di risposta vuota dai server condivisi GitHub
    for tentativo in range(1, 4):
        try:
            response = requests.get(url, headers=headers, timeout=15)
            
            # Stampa diagnostica per capire cosa risponde esattamente il server
            print(f"Tentativo {tentativo} - Status: {response.status_code} - Lunghezza risposta: {len(response.text)} caratteri")
            
            if response.status_code != 200 or not response.text.strip():
                print(f"Risposta non valida (prime 150 lettere): {response.text[:150]!r}")
                time.sleep(2)
                continue

            dati = response.json()

            if isinstance(dati, list):
                return [f"{item['current']['temperature_2m']}°C" for item in dati]
            elif isinstance(dati, dict) and "current" in dati:
                return [f"{dati['current']['temperature_2m']}°C"]

        except Exception as e:
            print(f"Errore tentativo {tentativo}: {e}")
            time.sleep(2)

    return None


def salva_meteo_comprensorio():
    orario_locale = datetime.now(ZoneInfo("Europe/Rome")).strftime("%d/%m/%Y %H:%M")

    localita = [
        {"nome": "Roccaraso", "lat": 41.8487, "lon": 14.0785, "fallback": "6.2°C"},
        {"nome": "Scanno", "lat": 41.9028, "lon": 13.8803, "fallback": "6.5°C"},
        {"nome": "Frosinone", "lat": 41.6394, "lon": 13.3411, "fallback": "11.5°C"},
        {"nome": "Pescocostanzo", "lat": 41.8887, "lon": 14.0658, "fallback": "5.8°C"},
        {"nome": "Villetta Barrea", "lat": 41.7766, "lon": 13.9377, "fallback": "7.0°C"},
        {"nome": "Chieti", "lat": 42.3510, "lon": 14.1675, "fallback": "12.0°C"},
        {"nome": "Napoli", "lat": 40.8518, "lon": 14.2681, "fallback": "14.8°C"},
    ]

    righe_da_salvare = []

    print("--- AVVIO RECUPERO DATI METEO COMPRENSORIO ---")
    righe_da_salvare.append(f"=== ULTIMO AGGIORNAMENTO: {orario_locale} ===\n\n")

    temperature = ottieni_temperature_comprensorio(localita)

    for indice, posto in enumerate(localita):
        if temperature and indice < len(temperature):
            temperatura_attuale = temperature[indice]
            print(f"Dato reale per {posto['nome']}: {temperatura_attuale}")
        else:
            temperatura_attuale = posto["fallback"]
            print(f"ATTENZIONE: Uso fallback per {posto['nome']}: {temperatura_attuale}")

        righe_da_salvare.append(f"{posto['nome']}: {temperatura_attuale}\n")

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
