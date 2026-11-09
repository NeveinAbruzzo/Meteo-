import time
from datetime import datetime
import requests


def ottieni_temperatura_singola(nome, lat, lon):
    url = "https://open-meteo.com"
    parametri = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m",
        "timezone": "Europe/Rome",
    }
    headers = {"Accept": "application/json"}

    try:
        print(f"Interrogazione API per {nome}...")
        response = requests.get(url, params=parametri, headers=headers, timeout=12)

        if response.status_code == 200:
            dati = response.json()
            if "current" in dati and "temperature_2m" in dati["current"]:
                temp = dati["current"]["temperature_2m"]
                try:
                    unita = dati["current_units"]["temperature_2m"]
                except Exception:
                    unita = "°C"
                return f"{temp}{unita}"
        else:
            print(
                f"-> Server ha risposto con codice {response.status_code} per {nome}"
            )

    except Exception as e:
        print(f"-> Errore durante la lettura di {nome}: {e}")

    return None


def salva_meteo_comprensorio():
    localita_da_monitorare = [
        {"nome": "Roccaraso", "lat": 41.8487, "lon": 14.0785},
        {"nome": "Castel di Sangro", "lat": 41.7850, "lon": 14.1047},
        {"nome": "Rivisondoli", "lat": 41.8677, "lon": 14.0664},
    ]

    orario_locale = datetime.now().strftime("%d/%m/%Y %H:%M")
    righe_da_salvare = []

    print(f"--- INIZIO EXTRAZIONE DATI ({orario_locale}) ---")

    for posto in localita_da_monitorare:
        risultato = ottieni_temperatura_singola(
            posto["nome"], posto["lat"], posto["lon"]
        )

        if risultato:
            riga = f"[{orario_locale}] {posto['nome']}: {risultato}\n"
            righe_da_salvare.append(riga)
            print(f"-> OK memorizzato: {riga.strip()}")

        # APPLICHIAMO UNA PAUSA DI SICUREZZA DI 2 SECONDI
        # Questo serve a non far insospettire i server di Open-Meteo
        print("Pausa di sicurezza prima della prossima città...")
        time.sleep(2)

    # Scrittura finale nel file Dati_meteo.txt
    if righe_da_salvare:
        try:
            with open("Dati_meteo.txt", "a", encoding="utf-8") as file:
                file.writelines(righe_da_salvare)
            print(
                f"--- SUCCESS: {len(righe_da_salvare)} righe scritte su Dati_meteo.txt ---"
            )
        except Exception as file_error:
            print(f"-> Errore di scrittura sul file: {file_error}")
    else:
        print(
            "--- ATTENZIONE: Nessun dato salvato, l'API ha bloccato tutte le richieste ---"
        )


if __name__ == "__main__":
    salva_meteo_comprensorio()
