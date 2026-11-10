import os
import time
import json
import urllib.request
import urllib.parse

# =======================================================
# 1. IMPOSTA L'ID DEL TUO BLOG
# =======================================================
BLOG_ID = "5866549180112140631"
nome_file_json = "chiave_google.json"

if not os.path.exists(nome_file_json):
    raise FileNotFoundError(f"Errore: Il file {nome_file_json} non è presente nel repository!")

with open(nome_file_json, 'r', encoding='utf-8') as f:
    key_data = json.load(f)

# 2. LEGGI I DATI DAL FILE DI TESTO LOCALE
nome_file_meteo = "Dati_meteo.txt"
if not os.path.exists(nome_file_meteo):
    raise FileNotFoundError(f"Errore: Il file {nome_file_meteo} non esiste!")

with open(nome_file_meteo, 'r', encoding='utf-8') as f:
    contenuto_meteo = f.read()

# 3. GENERA IL TOKEN MANUALE (ELIMINA IL BUG DELL'OROLOGIO)
# Usiamo direttamente requests ed oauth2 senza librerie pesanti di Google
import requests

print("Richiesta del token di accesso a Google...")
token_url = "https://googleapis.com"
payload = {
    "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
    "assertion": ""
}

# Generazione dell'asserzione JWT manuale per evitare il blocco del fuso orario
import jwt  # richiede pip install PyJWT cryptography
from jwt.algorithms import RSAAlgorithm

private_key_text = key_data["private_key"]
now = int(time.time())

# Impostiamo l'orario di inizio 2 minuti nel passato per fregare lo sfasamento dei server!
assertion_payload = {
    "iss": key_data["client_email"],
    "scope": "https://googleapis.com",
    "aud": token_url,
    "exp": now + 3600,
    "iat": now - 120  # Sfasamento intenzionale di sicurezza
}

assertion = jwt.encode(assertion_payload, private_key_text, algorithm="RS256")

# Richiesta token definitiva
r = requests.post(token_url, data={"grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer", "assertion": assertion})
if r.status_code != 200:
    raise RuntimeError(f"Errore nello sblocco del token Google: {r.text}")

access_token = r.json()["access_token"]
print("Token di accesso ottenuto con successo!")

# 4. PUBBLICA IL POST SU BLOGGER
contenuto_html = contenuto_meteo.replace('\n', '<br>')
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}
corpo_post = {
    "kind": "blogger#post",
    "title": "Aggiornamento Meteo Automatico",
    "content": contenido_html
}

url_blogger = f"https://googleapis.com{BLOG_ID}/posts"
res = requests.post(url_blogger, headers=headers, json=corpo_post)

if res.status_code == 200:
    print(f"🎉 CE L'ABBIAMO FATTA! Post pubblicato. ID: {res.json().get('id')}")
else:
    raise RuntimeError(f"Errore definitivo durante la pubblicazione su Blogger: {res.text}")
