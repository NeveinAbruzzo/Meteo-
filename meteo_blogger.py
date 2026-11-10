import os
import json
import requests
from google.oauth2 import credentials
from googleapiclient.discovery import build

# --- CONFIGURAZIONE ---
BLOG_ID = "IL_TUO_BLOG_ID"  # ⚠️ Sostituisci con l'ID numerico reale del tuo Blogger

def recupera_dati_meteo():
    url = "https://open-meteo.com"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            current = data["current_weather"]
            return f"Temperatura attuale: {current['temperature']}°C<br>Velocità del vento: {current['windspeed']} km/h"
    except Exception as e:
        print(f"Errore recupero meteo: {e}")
    return "Impossibile recuperare i dati meteo aggiornati."

def pubblica_su_blogger():
    secrets_raw = os.environ.get("BOM_GOOGLE_CREDENTIALS")
    if not secrets_raw:
        print("Errore: Secret BOM_GOOGLE_CREDENTIALS non trovato.")
        return
        
    creds_info = json.loads(secrets_raw)
    
    # Estraiamo i dati dal JSON scaricato da Google Cloud (struttura "web")
    if "web" in creds_info:
        web_info = creds_info["web"]
        creds = credentials.Credentials(
            token=None,
            refresh_token=web_info.get("refresh_token"), # Verrà letto se presente
            client_id=web_info.get("client_id"),
            client_secret=web_info.get("client_secret"),
            token_uri=web_info.get("token_uri", "https://googleapis.com")
        )
    else:
        creds = credentials.Credentials.from_authorized_user_info(creds_info)
    
    service = build('blogger', 'v3', credentials=creds)
    meteo_html = recupera_dati_meteo()
    
    body = {
        "kind": "blogger#post",
        "title": "Bollettino Meteo Aggiornato 🌤️",
        "content": f"<p>Ecco gli ultimi aggiornamenti meteo generati automaticamente:</p><p>{meteo_html}</p>",
        "labels": ["Meteo", "Automazione"]
    }
    
    try:
        request = service.posts().insert(blogId=BLOG_ID, body=body)
        response = request.execute()
        print(f"Post pubblicato con successo! URL: {response['url']}")
    except Exception as e:
        print(f"Errore durante la pubblicazione su Blogger: {e}")

if __name__ == "__main__":
    pubblica_su_blogger()
