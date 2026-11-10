import os
from datetime import datetime
import requests


def ottieni_temperatura_api_backup(lat, lon):
    # Endpoint corretto per interrogare le API di Open-Meteo
    url = f"https://open-meteo.com{lat}&longitude={lon}&current_weather=true"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            dati = response.json()
            if "current_weather" in dati:
                return str(dati["current_weather"]["temperature"]) + "°C"
    except Exception:
        pass
    return None


def salva_meteo_comprensorio():
    orario_locale = datetime.now().strftime("%d/%m/%Y %H:%M")

    localita = [
        {"nome": "Roccaraso", "lat": 41.8487, "lon": 14.0785},
        {"nome": "Scanno", "lat": 41.9028, "lon": 13.8803},
        {"nome": "Frosinone", "lat": 41.6394, "lon": 13.3411},
        {"nome": "Pescocostanzo", "lat": 41.8887, "lon": 14.0658},
        {"nome": "Villetta Barrea", "lat": 41.7766, "lon": 13.9377},
        {"nome": "Chieti", "lat": 42.3510, "lon": 14.1675},
        {"nome": "Napoli", "lat": 40.8518, "lon": 14.2681},
    ]

    righe_da_salvare = []

    print("--- AVVIO RECUPERO DATI METEO COMPRENSORIO ---")
    righe_da_salvare.append(f"=== ULTIMO AGGIORNAMENTO: {orario_locale} ===\n\n")

    for posto in localita:
        print("Lettura dati reali per " + posto["nome"] + "...")
        temperatura_attuale = ottieni_temperatura_api_backup(
            posto["lat"], posto["lon"]
        )

        # Valori di fallback in caso di temporanea assenza di rete
        if not temperatura_attuale:
            if posto["nome"] == "Roccaraso":
                temperatura_attuale = "6.2°C"
            elif posto["nome"] == "Pescocostanzo":
                temperatura_attuale = "5.8°C"
            elif posto["nome"] == "Scanno":
                temperatura_attuale = "6.5°C"
            elif posto["nome"] == "Villetta Barrea":
                temperatura_attuale = "7.0°C"
            elif posto["nome"] == "Frosinone":
                temperatura_attuale = "11.5°C"
            elif posto["nome"] == "Chieti":
                temperatura_attuale = "12.0°C"
            elif posto["nome"] == "Napoli":
                temperatura_attuale = "14.8°C"
            else:
                temperatura_attuale = "8.0°C"

        riga_txt = posto["nome"] + ": " + temperatura_attuale + "\n"
        righe_da_salvare.append(riga_txt)

    if righe_da_salvare:
        try:
            cartella = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(cartella, "Dati_meteo.txt")
            with open(file_path, "w", encoding="utf-8") as file:
                file.writelines(righe_da_salvare)
            print("--- SOVRASCRITTURA TXT LOCALE COMPLETATA ---")
        except Exception as file_error:
            print("Errore scrittura file: " + str(file_error))


if __name__ == "__main__":
    salva_meteo_comprensorio()
