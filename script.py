from datetime import datetime
import requests


def salva_meteo_open_meteo():
    # URL ufficiale corretto per le previsioni ed il meteo attuale
    url = "https://api.open-meteo.com/v1/forecast"

    # Parametri precisi per Roccaraso
    parametri = {
        "latitude": 41.8487,
        "longitude": 14.0785,
        "current": "temperature_2m",
        "timezone": "Europe/Rome",  # Forza il fuso orario corretto
    }

    # Header molto leggeri e puliti per evitare blocchi cloud da GitHub Actions
    headers = {"Accept": "application/json"}

    orario_locale = datetime.now().strftime("%d/%m/%Y %H:%M")

    try:
        print("Tentativo di connessione ai server di Open-Meteo...")
        response = requests.get(url, params=parametri, headers=headers, timeout=15)

        # Se il server risponde ma c'è un blocco (es. errore 429 per troppe richieste)
        if response.status_code != 200:
            print(
                f"-> API Bloccata. Codice Errore: {response.status_code}. Contenuto ricevuto: {response.text[:100]}"
            )
            return

        # Estrazione sicura del JSON
        dati = response.json()

        if "current" in dati:
            temperatura = dati["current"]["temperature_2m"]
            unita = dati["current_units"]["temperature_2m"]

            riga = f"[{orario_locale}] Roccaraso: {temperatura}{unita}\n"

            # Scrittura sul file con la D maiuscola come registrato su Git
            with open("Dati_meteo.txt", "a", encoding="utf-8") as file:
                file.write(riga)

            print(f"-> DATI REALI SALVATI CON SUCCESSO: {riga.strip()}")
        else:
            print("-> Errore: la struttura del JSON inviato da Open-Meteo è cambiata.")

    except Exception as e:
        print(f"-> ERRORE DI RETE CRITICO: {e}")


if __name__ == "__main__":
    salva_meteo_open_meteo()
