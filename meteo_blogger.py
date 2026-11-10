import os
import json
import urllib.request

# =======================================================
# 1. IMPOSTA L'ID DEL TUO BLOG
# Sostituisci questo numero con il numero reale del tuo blog!
# =======================================================
BLOG_ID = "5866549180112140631"

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

# 3. CHIAVE API INSERITA DIRETTAMENTE (PROVVISORIO PER TEST)
api_key = "AIzaSyBIwTIGpvAvurx-ljNvJ2fHcZI3mUyshPA"

if not api_key or api_key == "INCOLLA_QUI_LA_TUA_CHIAVE_API_REALE":
    raise ValueError("Errore: Inserisci la tua chiave API reale tra le virgolette per fare il test!")


# 4. PREPARA LA RICHIESTA HTTP DIRETTA PER BLOGGER
url = f"https://googleapis.com{BLOG_ID}/posts?key={api_key}"

# Trasforma i dati meteo in formato HTML per preservare gli a capo del testo
contenuto_html = contenuto_meteo.replace('\n', '<br>')

payload = {
    "kind": "blogger#post",
    "blog": {"id": BLOG_ID},
    "title": "Aggiornamento Meteo Automatico",
    "content": contenido_html
}

data_inserimento = json.dumps(payload).encode('utf-8')

req = urllib.request.Request(
    url, 
    data=data_inserimento, 
    headers={'Content-Type': 'application/json'}
)

# 5. INVIA I DATI A GOOGLE
try:
    with urllib.request.urlopen(req) as response:
        risposta_server = json.loads(response.read().decode('utf-8'))
        print(f"🎉 SUCCESSO! Dati meteo inviati a Blogger. ID Post: {risposta_server.get('id')}")
except Exception as e:
    raise RuntimeError(f"Errore durante l'invio a Blogger. Verifica la chiave o l'ID del blog: {e}")
