import os
import requests

def scarica_meteo():
    url = "https://open-meteo.com"
    
    try:
        # Effettua la chiamata impostando un User-Agent per evitare blocchi da GitHub
        headers = {'User-Agent': 'GitHubAction-MeteoBot/1.0'}
        response = requests.get(url, headers=headers, timeout=10)
        
        # Verifica se la risposta HTTP è 200 OK
        response.raise_for_status()
        
        # Converte in dizionario Python
        dati = response.json()
        
        # Estrae il valore corretto dall'oggetto 'current'
        temperatura = dati["current"]["temperature_2m"]
        unita = dati["current_units"]["temperature_2m"]
        
        print(f"Temperatura rilevata: {temperatura}{unita}")
        
        # Salva il valore in un file di testo (es. meteo.txt) per i passaggi successivi di Git
        with open("meteo.txt", "w", encoding="utf-8") as f:
            f.write(f"Temperatura attuale: {temperatura}{unita}")
            
    except requests.exceptions.HTTPError as http_err:
        print(f"Errore HTTP: {http_err}")
        exit(1)
    except requests.exceptions.JSONDecodeError:
        print("Errore: La risposta del server non è un JSON valido.")
        print("Risposta ricevuta:", response.text)
        exit(1)
    except KeyError:
        print("Errore: La struttura JSON è cambiata o manca la chiave 'temperature_2m'.")
        exit(1)

if __name__ == "__main__":
    scarica_meteo()

