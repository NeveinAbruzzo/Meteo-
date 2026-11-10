import os
import json
from googleapiclient.discovery import build

# =======================================================
# 1. IMPOSTA L'ID DEL TUO BLOG
# Sostituisci questo numero con il numero reale del tuo blog!
# =======================================================
BLOG_ID = "IL_TUO_ID_DEL_BLOG_QUI"

# 2. LEGGI I DATI DAL FILE DI TESTO LOCALE
nome_file_meteo = "Dati_meteo.txt"

if not os.path.exists(nome_file_meteo):
    raise FileNotFoundError(f"Errore: Il file {nome_file_meteo} non esiste nel repository!")

try:
    with open(nome_file_meteo, 'r', encoding='utf-8') as f:
        contenuto_meteo = f.read()
    print("Dati meteo letti con successo dal file locale.")
except Exception as e:
    raise RuntimeError(f"Errore durante la lettura del file: {e}")

# 3. RECUPERA LA CHIAVE API (Inserita direttamente come nel test precedente)
api_key = "LA_TUA_CHIAVE_API_REALE_QUI"

if not api_key or api_key == "LA_TUA_CHIAVE_API_REALE_QUI":
    raise ValueError("Errore: Inserisci la tua chiave API reale tra le virgolette!")

# 4. CONFIGURA IL SERVIZIO UFFICIALE DI GOOGLE
try:
    # Build gestisce l'URL internamente in modo sicuro senza usare urllib
    blogger_service = build('blogger', 'v3', developerKey=api_key)
    print("Connessione ai server di Google Blogger configurata.")
except Exception as e:
    raise RuntimeError(f"Errore durante la configurazione del servizio Google: {e}")

# 5. INVIA I DATI A GOOGLE
# Trasforma i dati meteo in formato HTML per preservare gli a capo del testo
contenuto_html = contenuto_meteo.replace('\n', '<br>')

corpo_del_post = {
    "kind": "blogger#post",
    "title": "Aggiornamento Meteo Automatico",
    "content": contenuto_html
}

try:
    # Esegue l'inserimento usando le funzioni ufficiali
    request = blogger_service.posts().insert(blogId=BLOG_ID, body=corpo_del_post)
    risposta_server = request.execute()
    print(f"🎉 SUCCESSO! Dati meteo inviati a Blogger. ID Post: {risposta_server.get('id')}")
except Exception as e:
    raise RuntimeError(f"Errore durante l'invio del post. Verifica la chiave o l'ID del blog: {e}")
