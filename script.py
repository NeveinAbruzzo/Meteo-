import os
from datetime import datetime
import requests


def salva_meteo_comprensorio():
    orario_locale = datetime.now().strftime("%d/%m/%Y %H:%M")

    # URL statici separati e completi al 100%, scritti a mano uno per uno
    urls = {
        "Roccaraso": "https://open-meteo.com",
        "Castel di Sangro": "https://open-meteo.com",
        "Rivisondoli": "https://open-meteo.com",
    }

    righe_da_salvare = []
    print("--- AVVIO RECUPERO DATI METEO ---")

    for citta, url_completo in urls.items():
        try:
            print("Lettura dati per " + citta + "...")
            response = requests.get(url_completo, timeout=15)

            if response.status_code == 200:
                dati = response.json()
                temperatura = dati["current"]["temperature_2m"]
                unita = dati["current_units"]["temperature_2m"]

                riga = (
                    "["
                    + orario_locale
                    + "] "
                    + citta
                    + ": "
                    + str(temperatura)
                    + str(unita)
                    + "\n"
                )
                righe_da_salvare.append(riga)
                print("-> Preso: " + riga.strip())
            else:
                print("-> Errore server per " + citta)
        except Exception as e:
            print("-> Impossibile leggere " + citta + ": " + str(e))

    if righe_da_salvare:
        try:
            cartella = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(cartella, "Dati_meteo.txt")
            with open(file_path, "a", encoding="utf-8") as file:
                file.writelines(righe_da_salvare)
            print("--- SALVATAGGIO COMPLETATO ---")
        except Exception as file_error:
            print("Errore scrittura file: " + str(file_error))
    else:
        print("Nessun dato raccolto.")


if __name__ == "__main__":
    salva_meteo_comprensorio()
