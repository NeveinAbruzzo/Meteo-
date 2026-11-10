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

# 3. CREDENZIALI DI SERVIZIO DIRETTE
# Incolla l'INTERO contenuto del file .json scaricato da Google Cloud tra le tre virgolette
credenziali_prive = """
INCOLLA_QUI_IL_CONTENUTO_DEL_FILE_JSON_DELL_ACCOUNT_DI_SERVIZIO
"""

# 4. CONFIGURA IL SERVIZIO UFFICIALE DI GOOGLE
info_credenziali = json.loads(credenziali_prive)
creds = service_account.Credentials.from_service_account_info(info_credenziali)
scoped_creds = creds.with_scopes(['https://googleapis.com'])
blogger_service = build('blogger', 'v3', credentials=scoped_creds)

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
</except Exception as e:
    raise RuntimeError(f"Errore finale di invio: {e}")
