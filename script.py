from datetime import datetime
from zoneinfo import ZoneInfo
import os
import time
import requests


def ottieni_temperatura_singola(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; NeveInAbruzzoBot/1.0)",
        "Accept": "application/json"
    }
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        dati = response.json()
        return f"{dati['current']['temperature_2m']}°C"
    except Exception as e:
        print(f"Errore chiamata ({url[:45]}...): {e}")
        return None


def salva_meteo_comprensorio():
    orario_locale = datetime.now(ZoneInfo("Europe/Rome")).strftime("%d/%m/%Y %H:%M")

    # Inserisci o modifica qui i link diretti presi da Open-Meteo per ogni città
    localita = [
        {
            "nome": "Roccaraso",
            "url": "https://api.open-meteo.com/v1/forecast?latitude=41.8487&longitude=14.0785&current=temperature_2m",
            "fallback": "6.2°C"
        },
        {
            "nome": "Scanno",
            "url": "https://api.open-meteo.com/v1/forecast?latitude=41.9044&longitude=13.8796&current=temperature_2m",
            "fallback": "6.5°C"
        },
        {
            "nome": "Frosinone",
            "url": "https://api.open-meteo.com/v1/forecast?latitude=41.6398&longitude=13.3411&current=temperature_2m",
            "fallback": "11.5°C"
        },
        {
            "nome": "Pescocostanzo",
            "url": "https://api.open-meteo.com/v1/forecast?latitude=41.8872&longitude=14.0661&current=temperature_2m",
            "fallback": "5.8°C"
        },
        {
            "nome": "Villetta Barrea",
            "url": "https://api.open-meteo.com/v1/forecast?latitude=41.7554&longitude=13.9909&current=temperature_2m",
            "fallback": "7.0°C"
        },
        {
            "nome": "Chieti",
            "url": "https://api.open-meteo.com/v1/forecast?latitude=42.3483&longitude=14.1649&current=temperature_2m",
            "fallback": "12.0°C"
        },
        {
            "nome": "Napoli",
            "url": "https://api.open-meteo.com/v1/forecast?latitude=40.8762&longitude=14.5195&current=temperature_2m",
            "fallback": "14.8°C"
        },
    ]

    righe_da_salvare = []

    print("--- AVVIO RECUPERO DATI METEO COMPRENSORIO ---")
    righe_da_salvare.append(f"=== ULTIMO AGGIORNAMENTO: {orario_locale} ===\n\n")

    for posto in localita:
        temperatura_attuale = ottieni_temperatura_singola(posto["url"])

        if temperatura_attuale is not None:
            print(f"Dato reale per {posto['nome']}: {temperatura_attuale}")
        else:
            temperatura_attuale = posto["fallback"]
            print(f"ATTENZIONE: Uso fallback per {posto['nome']}: {temperatura_attuale}")

        righe_da_salvare.append(f"{posto['nome']}: {temperatura_attuale}\n")
        
        # Piccola pausa di sicurezza per non sovraccaricare l'API tra una città e l'altra
        time.sleep(0.3)

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



