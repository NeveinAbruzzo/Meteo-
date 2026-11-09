from datetime import datetime
import requests


def salva_temperatura():
    # URL di base dell'API (senza i parametri agganciati)
    url_base = "https://api.open-meteo.com/v1/forecast"

    # Isoliamo i parametri così Python li compone senza errori di battitura
    parametri = {
        "latitude": 41.8487,
        "longitude": 14.0785,
        "current": "temperature_2m",
    }

    # Usiamo un'intestazione (User-Agent) che simula un browser reale per evitare blocchi anti-bot
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        # Effettuiamo la richiesta passando i parametri in modo esplicito
        response = requests.get(
            url_base, params=parametri, headers=headers, timeout=15
        )

        # Controlla se il server risponde con un errore HTTP (es. 404, 500)
        response.raise_for_status()

        # Verifica se la risposta è davvero un JSON e non una pagina HTML
        if "application/json" not in response.headers.get("Content-Type", ""):
            print("ATTENZIONE: Il server ha risposto con una pagina web HTML!")
            print("Controlla che l'URL sia corretto e non bloccato.")
            exit(1)

        dati = response.json()

        # Estraiamo i valori corretti dal JSON ottenuto
        temperatura = dati["current"]["temperature_2m"]
        unita = dati["current_units"]["temperature_2m"]

        # Otteniamo l'orario attuale per il report
        orario_locale = datetime.now().strftime("%d/%m/%Y %H:%M")
        riga_meteo = (
            f"[{orario_locale}] Temperatura rilevata: {temperatura}{unita}\n"
        )

        # Scriviamo nel file presente sul tuo repository
        with open("Dati_meteo.txt", "a", encoding="utf-8") as file:
            file.write(riga_meteo)

        print(f"Successo! Salvato nel file: {riga_meteo.strip()}")

    except Exception as e:
        print(f"Si è verificato un errore durante l'esecuzione: {e}")
        exit(1)


if __name__ == "__main__":
    salva_temperatura()
