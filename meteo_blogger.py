import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

# =======================================================
# 1. IMPOSTA L'ID DEL TUO BLOG
# =======================================================
# L'ID preso dal tuo log è 5866549180112140631
BLOG_ID = "5866549180112140631"

# 2. LEGGI I DATI DAL FILE DI TESTO LOCALE
nome_file_meteo = "Dati_meteo.txt"

if not os.path.exists(nome_file_meteo):
    raise FileNotFoundError(f"Errore: Il file {nome_file_meteo} non esiste nel repository!")

with open(nome_file_meteo, 'r', encoding='utf-8') as f:
    contenuto_meteo = f.read()

# 3. CARICA LE CREDENZIALI DIRETTAMENTE DAL FILE JSON CARICATO
nome_file_json = "chiave_google.json"

if not os.path.exists(nome_file_json):
    raise FileNotFoundError(f"Errore: Il file {nome_file_json} non è presente nel repository!")

# 4. CONFIGURA IL SERVIZIO UFFICIALE DI GOOGLE
try:
    creds = service_account.Credentials.from_service_account_file(
        nome_file_json,
        scopes=['https://googleapis.com']
    )
    blogger_service = build('blogger', 'v3', credentials=creds)
    print("Connessione ai server di Google Blogger configurata con successo.")
except Exception as e:
    raise RuntimeError(f"Errore durante la configurazione delle credenziali Google: {e}")

# 5. INVIA I DATI A GOOGLE
contenuto_html = contenuto_meteo.replace('\n', '<br>')

corpo_del_post = {
    "kind": "blogger#post",
    "title": "Aggiornamento Meteo Automatico",
    "content": contenuto_html
}

try:
    request = blogger_service.posts().insert(blogId=BLOG_ID, body=corpo_del_post)
    risposta_server = request.execute()
    print(f"🎉 CE L'ABBIAMO FATTA! Post pubblicato sul blog. ID Post: {risposta_server.get('id')}")
except Exception as e:
    raise RuntimeError(f"Errore finale di invio: {e}")
