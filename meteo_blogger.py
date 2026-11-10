import os
import json
import requests
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# --- CONFIGURAZIONE ---
# ⚠️ SOSTITUISCI QUESTO ID CON QUELLO REALE DEL TUO BLOG BLOGGER
BLOG_ID = "5866549180112140631"  

def recupera_dati_meteo():
    """
    Recupera i dati meteo in tempo reale da Open-Meteo per usarli nel post.
    Puoi modificare latitude e longitude con le coordinate della tua città.
    """
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
    # 1. Recupera il JSON dalle credenziali segrete di GitHub
    secrets_raw = os.environ.get("BOM_GOOGLE_CREDENTIALS")  # Cambia il nome se lo hai chiamato diversamente nei Secret
    if not secrets_raw:
        print("Errore: Secret BOM_GOOGLE_CREDENTIALS non trovato su GitHub.")
        return
        
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# ... all'interno di pubblica_su_blogger():
creds_info = json.loads(secrets_raw)

# Se il file contiene la struttura "web", usiamo il caricamento corretto del client config
if "web" in creds_info:
    # Definiamo i permessi richiesti per Blogger
    SCOPES = ['https://googleapis.com']
    flow = InstalledAppFlow.from_client_config(creds_info, scopes=SCOPES)
    # Nota: Questo metodo potrebbe richiedere un'autenticazione interattiva la prima volta.
    # Se gira su GitHub Actions in modo non interattivo, potrebbe essere necessario usare un account di servizio o inserire il refresh token.
    creds = flow.credentials
else:
    creds = Credentials.from_authorized_user_info(creds_info)









    
    
    # 2. Inizializza il servizio Blogger API
    service = build('blogger', 'v3', credentials=creds)
    
    # 3. Genera il contenuto HTML del post
    meteo_html = recupera_dati_meteo()
    
    body = {
        "kind": "blogger#post",
        "title": "Bollettino Meteo Aggiornato 🌤️",
        "content": f"<p>Ecco gli ultimi aggiornamenti meteo generati automaticamente:</p><p>{meteo_html}</p>",
        "labels": ["Meteo", "Automazione", "OpenMeteo"]
    }
    
    # 4. Invia il post a Blogger
    try:
        request = service.posts().insert(blogId=BLOG_ID, body=body)
        response = request.execute()
        print(f"Post pubblicato con successo! Link: {response['url']}")
    except Exception as e:
        print(f"Errore durante la pubblicazione su Blogger: {e}")

if __name__ == "__main__":
    pubblica_su_blogger()

