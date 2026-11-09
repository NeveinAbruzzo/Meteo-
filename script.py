from datetime import datetime
import requests


def test_meteo_wttr():
    # Usiamo wttr.in specificando la città e il formato JSON (format=j1)
    url = "https://wttr.in"

    orario_locale = datetime.now().strftime("%d/%m/%Y %H:%M")

    try:
        print("Interrogazione API wttr.in per Roccaraso...")
        response = requests.get(url, timeout=15)

        if response.status_code != 200:
            print(
                f"-> Il server ha risposto con codice {response.status_code}."
            )
            return

        dati = response.json()

        # Estrazione della temperatura attuale dal JSON di wttr.in
        temperatura = dati["current_condition"][0]["temp_C"]

        riga = f"[{orario_locale}] Roccaraso: {temperatura}°C\n"

        # Scrittura sul file mantenendo la D maiuscola
        with open("Dati_meteo.txt", "a", encoding="utf-8") as file:
            file.write(riga)

        print(f"-> SCRITTURA RIUSCITA: {riga.strip()}")

    except Exception as e:
        print(f"-> ERRORE CRITICO: {e}")


if __name__ == "__main__":
    test_meteo_wttr()
