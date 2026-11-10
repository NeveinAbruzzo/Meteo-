import os
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# ==========================================
# 1. LEGGI I DATI DAL FILE DI TESTO LOCALE
# ==========================================
nome_file_meteo = "Dati_meteo.txt"

if not os.path.exists(nome_file_meteo):
    raise FileNotFoundError(f"Errore: Il file {nome_file_meteo} non è stato trovato!")

try:
    with open(nome_file_meteo, 'r', encoding='utf-8') as f:
        contenuto_meteo = f.read()
    print("Dati meteo letti con successo dal file locale.")
except Exception as e:
    raise RuntimeError(f"Errore durante la lettura del file di testo: {e}")


# ==========================================
# 2. AUTENTICAZIONE CON GOOGLE BLOGGER
# ==========================================
# Recupera il JSON delle credenziali dai Secrets di GitHub
credenziali_json = os.environ.get('BOM_GOOGLE_CREDENTIALS')
# INSERISCI QUI IL TUO ID DEL BLOG DI BLOGGER
BLOG_ID = "5866549180112140631" 

if not credenziali_json:
    raise ValueError("Errore: La variabile d'ambiente GOOGLE_CREDENTIALS è vuota o mancante nei Repository Secrets!")

try:
    info_credenziali = json.loads(credenziali_json)
    creds = Credentials.from_authorized_user_info(info_credenziali)
    blogger_service = build('blogger', 'v3', credentials=creds)
    print("Autenticazione con Google Blogger riuscita.")
except Exception as e:
    raise RuntimeError(f"Errore durante l'autenticazione con Blogger: {e}")


# ==========================================
# 3. PUBBLICAZIONE DEL POST
# ==========================================
corpo_del_post = {
    'kind': 'blogger#post',
    'title': 'Aggiornamento Meteo Automatico',
    'content': contenuto_meteo  # Inserisce il testo del file pari pari
}

try:
    # Esegue la pubblicazione ufficiale
    request = blogger_service.posts().insert(blogId=BLOG_ID, body=corpo_del_post)
    response = request.execute()
    print(f"Post pubblicato con successo! URL: {response.get('url')}")
except Exception as e:
    raise RuntimeError(f"Errore durante la pubblicazione del post: {e}")
