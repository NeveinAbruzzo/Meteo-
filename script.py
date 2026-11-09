from datetime import datetime
import requests


def salva_meteo_multiplo():
    # URL CORRETTO per interrogare l'API di Open-Meteo
    url_base = "https://open-meteo.com"

    citta_da_monitorare = [
        {"nome": "Pescasseroli", "lat": 41.8487, "lon": 14.0785},
        {"nome": "Roma", "lat": 41.8919, "lon": 12.5113},
        {"nome": "Milano", "lat": 45.4642, "lon": 9.1900},
    ]

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    orario_locale = datetime.now().strftime("%d/%m/%Y %H:%M")
    righe_da_salvare = []

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

            dati = response.json()
            temperatura = dati["current"]["temperature_2m"]
            unita = dati["current_units"]["temperature_2m"]

            riga = f"[{orario_locale}] {citta['nome']}: {temperatura}{unita}\n"
            righe_da_salvare.append(riga)
            print(f"Recuperato con successo: {riga.strip()}")

        except Exception as e:
            print(f"Errore con la città {citta['nome']}: {e}")

    if righe_da_salvare:
        # Scrive nel file mantenendo la D maiuscola come da tua struttura
        with open("Dati_meteo.txt", "a", encoding="utf-8") as file:
            file.writelines(righe_da_salvare)
        print(f"Scritte {len(righe_da_salvare)} righe su Dati_meteo.txt")
    else:
        print("Nessun dato scritto: la lista delle righe è vuota.")


if __name__ == "__main__":
    salva_meteo_multiplo()
