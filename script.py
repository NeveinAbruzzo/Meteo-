from datetime import datetime
import requests


def salva_meteo_comprensorio():
    # URL ufficiale corretto per Open-Meteo
    url = "https://open-meteo.com"

    # Elenco delle 3 località richieste con le rispettive coordinate geografiche
    localita_da_monitorare = [
        {"nome": "Roccaraso", "lat": 41.8487, "lon": 14.0785},
        {"nome": "Castel di Sangro", "lat": 41.7850, "lon": 14.1047},
        {"nome": "Rivisondoli", "lat": 41.8677, "lon": 14.0664},
    ]

    headers = {"Accept": "application/json"}
    orario_locale = datetime.now().strftime("%d/%m/%Y %H:%M")
    righe_da_salvare = []

    print(f"--- INIZIO MONITORAGGIO ({orario_locale}) ---")

    for posto in localita_da_monitorare:
        parametri = {
            "latitude": posto["lat"],
            "longitude": posto["lon"],
            "current": "temperature_2m",
            "timezone": "Europe/Rome",
        }

        try:
            print(f"Richiesta dati per {posto['nome']}...")
            response = requests.get(url, params=parametri, headers=headers, timeout=15)

            if response.status_code != 200:
                print(f"-> Errore con {posto['nome']} (Codice HTTP {response.status_code})")
                continue

            dati = response.json()

            if "current" in dati:
                temperatura = dati["current"]["temperature_2m"]
                unita = dati["current_units"]["temperature_2m"]

                riga = f"[{orario_locale}] {posto['nome']}: {temperatura}{unita}\n"
                righe_da_salvare.append(riga)
                print(f"-> Recuperato: {riga.strip()}")
            else:
                print(f"-> Struttura JSON non valida per {posto['nome']}")

        except Exception as e:
            print(f"-> Errore di rete con {posto['nome']}: {e}")

    # Scrittura cumulativa per evitare di aprire e chiudere il file più volte
    if righe_da_salvare:
        try:
            with open("Dati_meteo.txt", "a", encoding="utf-8") as file:
                file.writelines(righe_da_salvare)
            print(f"--- SUCCESS: {len(righe_da_salvare)} righe scritte su Dati_meteo.txt ---")
        except Exception as file_error:
            print(f"-> Errore critico di scrittura sul file: {file_error}")
    else:
        print("--- ATTENZIONE: Nessun dato salvato in questa sessione ---")


if __name__ == "__main__":
    salva_meteo_comprensorio()
