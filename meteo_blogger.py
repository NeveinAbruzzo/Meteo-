import os

# 1. LEGGI I DATI DAL FILE DI TESTO LOCALE
nome_file_meteo = "Dati_meteo.txt"

if not os.path.exists(nome_file_meteo):
    raise FileNotFoundError(f"Errore: Il file {nome_file_meteo} non è stato trovato nel repository!")

try:
    with open(nome_file_meteo, 'r', encoding='utf-8') as f:
        contenuto_meteo = f.read()
    print("Dati meteo letti con successo dal file locale.")
except Exception as e:
    raise RuntimeError(f"Errore durante la lettura del file di testo: {e}")

# 2. CONFIGURA IL CONTENUTO PER BLOGGER
# Ora la variabile 'contenuto_meteo' contiene il testo esatto del tuo file.
# Puoi usarla direttamente nel corpo del post di Blogger, ad esempio:
titolo_post = "Aggiornamento Meteo Automatico"
corpo_post = contenuto_meteo  # Trasferisce il testo pari pari
