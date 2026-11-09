from datetime import datetime
import requests


def salva_temperatura():
    # URL dell'API Open-Meteo
    url = "https://open-meteo.com"

    try:
        # Aggiungiamo un User-Agent standard per evitare blocchi di rete
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers, timeout=15)

        # Controlla se la risposta del server è un errore HTTP (es. 404, 500)
        response.raise_for_status()

        # Proviamo a decodificare il JSON
        try:
            dati = response.json()
        except Exception:
            print("Il server non ha restituito un JSON valido!")
            print("Contenuto ricevuto dal server:", response.text)
            raise

        # Estraiamo i valori corretti
        temperatura = dati["current"]["temperature_2m"]
        unita = dati["current_units"]["temperature_2m"]

        # Otteniamo l'orario attuale per il report
        orario_locale = datetime.now().strftime("%d/%m/%Y %H:%M")
        riga_meteo = (
            f"[{orario_locale}] Temperatura rilevata: {temperatura}{unita}\n"
        )

        # Scriviamo nel file corretto presente sul tuo repository (Dati_meteo.txt)
        with open("Dati_meteo.txt", "a", encoding="utf-8") as file:
            file.write(riga_meteo)

        print(f"Successo! Salvato nel file: {riga_meteo.strip()}")

    except Exception as e:
        print(f"Si è verificato un errore durante l'esecuzione: {e}")
        exit(1)


if __name__ == "__main__":
    salva_temperatura()
