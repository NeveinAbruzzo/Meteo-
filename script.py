from datetime import datetime
import requests


def test_meteo_singolo():
    # URL ufficiale completo
    url = "https://open-meteo.com"

    # Parametri espliciti per Roccaraso
    parametri = {
        "latitude": 41.8487,
        "longitude": 14.0785,
        "current": "temperature_2m",
        "format": "json",  # Forza il formato JSON in uscita
    }

    orario_locale = datetime.now().strftime("%d/%m/%Y %H:%M")

    try:
        print("Interrogazione API di Open-Meteo per Roccaraso...")

        # Facciamo una richiesta pulita senza header personalizzati che possono insospettire i server
        response = requests.get(url, params=parametri, timeout=15)

        # Se l'API risponde con un errore (es. 403 o 404), questo lo intercetta subito
        if response.status_code != 200:
            print(
                f"-> Il server ha risposto con codice {response.status_code}. Contenuto: {response.text[:100]}"
            )
            return

        dati = response.json()

        if "current" in dati:
            temperatura = dati["current"]["temperature_2m"]
            unita = dati["current_units"]["temperature_2m"]

            riga = f"[{orario_locale}] Roccaraso: {temperatura}{unita}\n"

            # Scrittura sul file con la D maiuscola
            with open("Dati_meteo.txt", "a", encoding="utf-8") as file:
                file.write(riga)

            print(f"-> SCRITTURA RIUSCITA: {riga.strip()}")
        else:
            print(
                f"-> Struttura JSON imprevista. Chiavi ricevute: {list(dati.keys())}"
            )

    except Exception as e:
        print(f"-> ERRORE CRITICO: {e}")


if __name__ == "__main__":
    test_meteo_singolo()
