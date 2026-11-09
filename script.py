from datetime import datetime
import requests


def salva_temperatura():
    url = "https://open-meteo.com"

    try:
        headers = {"User-Agent": "MeteoBot/1.0"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        dati = response.json()
        temperatura = dati["current"]["temperature_2m"]
        unita = dati["current_units"]["temperature_2m"]

        orario_locale = datetime.now().strftime("%d/%m/%Y %H:%M")
        riga_meteo = (
            f"[{orario_locale}] Temperatura rilevata: {temperatura}{unita}\n"
        )

        with open("diario_meteo.txt", "a", encoding="utf-8") as file:
            file.write(riga_meteo)

        print(f"Successo! Salvato: {riga_meteo.strip()}")

    except Exception as e:
        print(f"Si è verificato un errore: {e}")
        exit(1)


if __name__ == "__main__":
    salva_temperatura()
