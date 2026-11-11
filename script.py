from datetime import datetime
import os
import requests


def ottieni_temperature_comprensorio(localita):
    # Prepara le liste di latitudini e longitudini separate da virgola
    latitudini = ",".join(str(posto["lat"]) for posto in localita)
    longitudini = ",".join(str(posto["lon"]) for posto in localita)

    url = (
        f"https://open-meteo.com"
        f"?latitude={latitudini}&longitude={longitudini}"
        f"&current=temperature_2m&timezone=Europe%2FRome"
    )

    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        dati = response.json()

        # Se c'è più di una località, Open-Meteo restituisce una lista di dizionari
        if isinstance(dati, list):
            return [
                f"{item['current']['temperature_2m']}°C" for item in dati
            ]
        # Caso di sicurezza se ci fosse una sola località
        elif isinstance(dati, dict) and "current" in dati:
            return [f"{dati['current']['temperature_2m']}°C"]

    except Exception as e:
        print(f"Errore durante il recupero dei dati da Open-Meteo: {e}")

    return None


def salva_meteo_comprensorio():
    orario_locale = datetime.now().strftime("%d/%m/%Y %H:%M")

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
