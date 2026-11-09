from datetime import datetime
import requests


def test_meteo_singolo():
    url_base = "https://open-meteo.com"

    # Coordinate geografiche precise di Roccaraso
    parametri = {
        "latitude": 41.8487,
        "longitude": 14.0785,
        "current": "temperature_2m",
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    orario_locale = datetime.now().strftime("%d/%m/%Y %H:%M")

    try:
        print("Interrogazione API di Open-Meteo per Roccaraso...")
        response = requests.get(
            url_base, params=parametri, headers=headers, timeout=15
        )
        response.raise_for_status()

        dati = response.json()
        temperatura = dati["current"]["temperature_2m"]
        unita = dati["current_units"]["temperature_2m"]

        riga = f"[{orario_locale}] Roccaraso: {temperatura}{unita}\n"

        # Scrittura diretta sul file con la "D" maiuscola
        with open("Dati_meteo.txt", "a", encoding="utf-8") as file:
            file.write(riga)

        print(f"-> SCRITTURA RIUSCITA: {riga.strip()}")

    except Exception as e:
        print(f"-> ERRORE CRITICO: {e}")


if __name__ == "__main__":
    test_meteo_singolo()
