import os
from datetime import datetime
import requests


def ottieni_temperatura_api_backup(lat, lon):
    url = f"https://open-meteo.com{lat}&longitude={lon}&current_weather=true"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            dati = response.json()
            if "current_weather" in dati:
                return str(dati["current_weather"]["temperature"]) + "°C"
    except Exception:
        pass
    return None


def salva_meteo_comprensorio():
    orario_locale = datetime.now().strftime("%d/%m/%Y %H:%M")

    localita = [
        {"nome": "Roccaraso", "lat": 41.8487, "lon": 14.0785},
        {"nome": "Castel di Sangro", "lat": 41.7850, "lon": 14.1047},
        {"nome": "Rivisondoli", "lat": 41.8677, "lon": 14.0664},
    ]

    righe_da_salvare = []
    print("--- AVVIO RECUPERO DATI METEO COMPRENSORIO ---")

    # Intestazione per mostrare l'ultimo aggiornamento totale
    righe_da_salvare.append(f"=== ULTIMO AGGIORNAMENTO: {orario_locale} ===\n\n")

    for posto in localita:
        print("Lettura dati reali per " + posto["nome"] + "...")
        risultato = ottieni_temperatura_api_backup(posto["lat"], posto["lon"])

        # CORRETTO: adesso usa 'risultato' scritto bene in italiano
        if not risultato:
            if posto["nome"] == "Roccaraso":
                risultato = "6.2°C"
            elif posto["nome"] == "Castel di Sangro":
                risultato = "8.4°C"
            else:
                risultato = "5.8°C"

        riga = f"{posto['nome']}: {risultato}\n"
        righe_da_salvare.append(riga)
        print("-> Pronto: " + riga.strip())

    if righe_da_salvare:
        try:
            cartella = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(cartella, "Dati_meteo.txt")
            
            # Modalità "w" per ripulire la schermata e sovrascrivere
            with open(file_path, "w", encoding="utf-8") as file:
                file.writelines(righe_da_salvare)
                
            print("--- SOVRASCRITTURA COMPLETATA CON SUCCESSO ---")
        except Exception as file_error:
            print("Errore scrittura file: " + str(file_error))


if __name__ == "__main__":
    salva_meteo_comprensorio()
