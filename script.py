from datetime import datetime
import requests


def salva_meteo_multiplo():
    url_base = "https://open-meteo.com"

    # 1. Elenco delle città che vuoi monitorare. Puoi aggiungerne quante ne vuoi!
    citta_da_monitorare = [
        {"nome": "Pescasseroli", "lat": 41.8487, "lon": 14.0785},
        {"nome": "Roma", "lat": 41.8919, "lon": 12.5113},
        {"nome": "Milano", "lat": 45.4642, "lon": 9.1900},
    ]

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    # Otteniamo l'orario attuale una sola volta per tutte le letture
    orario_locale = datetime.now().strftime("%d/%m/%Y %H:%M")
    righe_da_salvare = []

    # 2. Il ciclo gira per ogni città presente nella lista
    for citta in citta_da_monitorare:
        parametri = {
            "latitude": citta["lat"],
            "longitude": citta["lon"],
            "current": "temperature_2m",
        }

        try:
            response = requests.get(
                url_base, params=parametri, headers=headers, timeout=15
            )
            response.raise_for_status()

            if "application/json" not in response.headers.get(
                "Content-Type", ""
            ):
                print(
                    f"Errore: Risposta non valida per la città {citta['nome']}"
                )
                continue

            dati = response.json()

            # Estraiamo la temperatura
            temperatura = dati["current"]["temperature_2m"]
            unita = dati["current_units"]["temperature_2m"]

            # Prepariamo la riga includendo il NOME della città
            riga = f"[{orario_locale}] {citta['nome']}: {temperatura}{unita}\n"
            righe_da_salvare.append(riga)
            print(f"Recuperato: {riga.strip()}")

        except Exception as e:
            print(f"Errore con la città {citta['nome']}: {e}")

    # 3. Scriviamo tutte le letture nel file Dati_meteo.txt in un colpo solo
    if righe_da_salvare:
        with open("Dati_meteo.txt", "a", encoding="utf-8") as file:
            file.writelines(righe_da_salvare)
        print("Tutte le città sono state salvate con successo!")


if __name__ == "__main__":
    salva_meteo_multiplo()
