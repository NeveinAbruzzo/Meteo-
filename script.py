import os
import time
from datetime import datetime
import requests


def ottieni_temperatura_wttr(nome_citta):
    # Sostituiamo gli spazi con il '+' (fondamentale per 'Castel+di+Sangro')
    citta_formattata = nome_citta.replace(" ", "+")
    
    # Costruiamo l'URL unendo le stringhe in modo classico, senza rischiare errori di f-string
    url = "https://wttr.in" + citta_formattata + "?format=j1"

    try:
        print("Interrogazione API wttr.in per " + nome_citta + "...")
        response = requests.get(url, timeout=12)

        if response.status_code == 200:
            dati = response.json()
            # Estrazione sicura della temperatura attuale
            temp = dati["current_condition"][0]["temp_C"]
            return temp + "°C"
        else:
            print("-> Il server ha risposto con codice " + str(response.status_code) + " per " + nome_citta)
    except Exception as e:
        print("-> Errore durante la lettura di " + nome_citta + ": " + str(e))

    return None


def salva_meteo_comprensorio():
    localita_da_monitorare = ["Roccaraso", "Castel di Sangro", "Rivisondoli"]

    orario_locale = datetime.now().strftime("%d/%m/%Y %H:%M")
    righe_da_salvare = []

    print("--- INIZIO EXTRAZIONE DATI (" + orario_locale + ") ---")

    for i, citta in enumerate(localita_da_monitorare):
        risultato = ottieni_temperatura_wttr(citta)

        if risultato:
            riga = "[" + orario_locale + "] " + citta + ": " + risultato + "\n"
            righe_da_salvare.append(riga)
            print("-> OK memorizzato: " + riga.strip())

        if i < len(localita_da_monitorare) - 1:
            time.sleep(1)

    # Scrittura finale nel file Dati_meteo.txt con percorso assoluto sicuro
    if righe_da_salvare:
        try:
            cartella_corrente = os.path.dirname(os.path.abspath(__file__))
            percorso_file = os.path.join(cartella_corrente, "Dati_meteo.txt")

            with open(percorso_file, "a", encoding="utf-8") as file:
                file.writelines(righe_da_salvare)
            print("--- SUCCESS: " + str(len(righe_da_salvare)) + " righe scritte correttamente ---")
        except Exception as file_error:
            print("-> Errore di scrittura sul file: " + str(file_error))
    else:
        print("--- ATTENZIONE: Nessun dato salvato ---")


if __name__ == "__main__":
    salva_meteo_comprensorio()
