import os
import time
from datetime import datetime
import requests


def ottieni_temperatura_wttr(nome_citta):
    #wttr.in permette di richiedere il meteo di qualsiasi città in formato JSON pulito (?format=j1)
    url = f"https://wttr.in{nome_citta}?format=j1"

    try:
        print(f"Interrogazione API wttr.in per {nome_citta}...")
        response = requests.get(url, timeout=12)

        if response.status_code == 200:
            dati = response.json()
            # Estrazione della temperatura attuale dal formato JSON di wttr.in
            temp = dati["current_condition"][0]["temp_C"]
            return f"{temp}°C"
        else:
            print(f"-> Il server ha risposto con codice {response.status_code} per {nome_citta}")
    except Exception as e:
        print(f"-> Errore durante la lettura di {nome_citta}: {e}")

    return None


def salva_meteo_comprensorio():
    # Elenco delle tre città dell'Alto Sangro
    localita_da_monitorare = ["Roccaraso", "Castel di Sangro", "Rivisondoli"]

    orario_locale = datetime.now().strftime("%d/%m/%Y %H:%M")
    righe_da_salvare = []

    print(f"--- INIZIO EXTRAZIONE DATI ({orario_locale}) ---")

    for i, citta in enumerate(localita_da_monitorare):
        risultato = ottieni_temperatura_wttr(citta)

        if risultato:
            riga = f"[{orario_locale}] {citta}: {risultato}\n"
            righe_da_salvare.append(riga)
            print(f"-> OK memorizzato: {riga.strip()}")

        # Piccola pausa di cortesia tra le chiamate
        if i < len(localita_da_monitorare) - 1:
            time.sleep(1)

    # Scrittura finale nel file Dati_meteo.txt con percorso assoluto sicuro
    if righe_da_salvare:
        try:
            cartella_corrente = os.path.dirname(os.path.abspath(__file__))
            percorso_file = os.path.join(cartella_corrente, "Dati_meteo.txt")

            with open(percorso_file, "a", encoding="utf-8") as file:
                file.writelines(righe_da_salvare)
            print(f"--- SUCCESS: {len(righe_da_salvare)} righe scritte correttamente in {percorso_file} ---")
        except Exception as file_error:
            print(f"-> Errore di scrittura sul file: {file_error}")
    else:
        print("--- ATTENZIONE: Nessun dato salvato ---")


if __name__ == "__main__":
    salva_meteo_comprensorio()
