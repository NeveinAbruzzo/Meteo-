from datetime import datetime
import requests


def salva_meteo_multiplo():
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

    print(f"--- INIZIO SCRIPT METEO ({orario_locale}) ---")

    for citta in citta_da_monitorare:
        parametri = {
            "latitude": citta["lat"],
            "longitude": citta["lon"],
            "current": "temperature_2m",
        }

        try:
            print(f"Richiesta dati per {citta['nome']}...")
            response = requests.get(
                url_base, params=parametri, headers=headers, timeout=15
            )

            # Mostra lo stato della risposta HTTP
            print(f"Risposta ricevuta da Open-Meteo: {response.status_code}")
            response.raise_for_status()

            dati = response.json()

            # Verifichiamo se le chiavi esistono nel JSON ricevuto
            if "current" in dati and "temperature_2m" in dati["current"]:
                temperatura = dati["current"]["temperature_2m"]
                unita = dati["current_units"]["temperature_2m"]

                riga = f"[{orario_locale}] {citta['nome']}: {temperatura}{unita}\n"
                righe_da_salvare.append(riga)
                print(f"-> OK, riga creata: {riga.strip()}")
            else:
                print(
                    f"-> ATTENZIONE: Struttura dati non valida nel JSON di {citta['nome']}"
                )

        except Exception as e:
            print(f"-> ERRORE con la città {citta['nome']}: {e}")

    print(f"Totale righe pronte per la scrittura: {len(righe_da_salvare)}")

    if righe_da_salvare:
        try:
            with open("Dati_meteo.txt", "a", encoding="utf-8") as file:
                file.writelines(righe_da_salvare)
            print("-> SUCCESS: Scrittura su file Dati_meteo.txt completata locali!")
        except Exception as file_error:
            print(f"-> ERRORE critico durante l'apertura/scrittura del file: {file_error}")
    else:
        print("-> ATTENZIONE: Nessun dato scritto perché la lista è vuota!")

    print("--- FINE SCRIPT METEO ---")


if __name__ == "__main__":
    salva_meteo_multiplo()
