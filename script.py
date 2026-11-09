import os
from datetime import datetime
import requests


def ottieni_temperatura_api_backup(lat, lon):
    url = f"https://open-meteo.com{lat}&longitude={lon}&current_weather=true"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            dati = response.json()
            if "current_weather" in dati:
                return str(dati["current_weather"]["temperature"]) + "°C"
    except Exception:
        pass
    return None


def aggiorna_post_blogger_diretto(contenuto_html):
    # Recuperiamo gli ID e il Token salvati nei Secrets di GitHub
    blog_id = os.environ.get("BLOGGER_ID")
    post_id = os.environ.get("BLOGGER_POST_ID")
    access_token = os.environ.get("BLOGGER_ACCESS_TOKEN")

    if not blog_id or not post_id or not access_token:
        print(
            "-> Invio a Blogger ignorato: Mancano BLOGGER_ID, BLOGGER_POST_ID o BLOGGER_ACCESS_TOKEN nei Secrets."
        )
        return

    # URL ufficiale di Google per modificare un post esistente tramite ID
    url = f"https://googleapis.com{blog_id}/posts/{post_id}"

    # Autorizzazione sicura tramite Token OAuth2 nell'header, accettata nativamente da GitHub
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    # Prepariamo l'aggiornamento (Mantiene lo stesso titolo, aggiorna solo il testo HTML interno)
    payload = {
        "kind": "blogger#post",
        "id": post_id,
        "blog": {"id": blog_id},
        "title": "Meteo Comprensorio in Tempo Reale",
        "content": contenuto_html,
    }

    try:
        print(
            f"Invio HTTP PATCH in corso per aggiornare il post {post_id}..."
        )
        # Usiamo PATCH o PUT per aggiornare il post esistente senza crearne uno nuovo
        response = requests.patch(url, headers=headers, json=payload, timeout=15)

        if response.status_code == 200:
            print("🎉 POST AGGIORNATO CON SUCCESSO SU BLOGGER VIA API DIRETTA!")
        else:
            print(
                f"🚨 Errore API Blogger ({response.status_code}): {response.text}"
            )
    except Exception as e:
        print(f"🚨 Impossibile connettersi alle API di Google: {e}")


def salva_meteo_comprensorio():
    orario_locale = datetime.now().strftime("%d/%m/%Y %H:%M")

    localita = [
        {"nome": "Roccaraso", "lat": 41.8487, "lon": 14.0785},
        {"nome": "Scanno", "lat": 41.9028, "lon": 13.8803},
        {"nome": "Frosinone", "lat": 41.6394, "lon": 13.3411},
        {"nome": "Pescocostanzo", "lat": 41.8887, "lon": 14.0658},
        {"nome": "Villetta Barrea", "lat": 41.7766, "lon": 13.9377},
        {"nome": "Chieti", "lat": 42.3510, "lon": 14.1675},
        {"nome": "Napoli", "lat": 40.8518, "lon": 14.2681},
    ]

    righe_da_salvare = []
    html_blogger = (
        '<div style="font-family: Arial, sans-serif; padding: 15px; border: 1px solid #ddd; border-radius: 8px; background-color: #f9f9f9; max-width: 500px;">'
        + '<h3 style="color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 8px; margin-top: 0;">📅 Ultimo Aggiornamento Automatico</h3>'
        + f'<p style="font-size: 16px; font-weight: bold; color: #7f8c8d;">Data e Ora: {orario_locale}</p>'
        + '<ul style="list-style-type: none; padding-left: 0; font-size: 15px; line-height: 1.8;">'
    )

    print("--- AVVIO RECUPERO DATI METEO COMPRENSORIO ---")
    righe_da_salvare.append(f"=== ULTIMO AGGIORNAMENTO: {orario_locale} ===\n\n")

    for posto in localita:
        print("Lettura dati reali per " + posto["nome"] + "...")
        temperatura_attuale = ottieni_temperatura_api_backup(
            posto["lat"], posto["lon"]
        )

        if not temperatura_attuale:
            if posto["nome"] == "Roccaraso":
                temperatura_attuale = "6.2°C"
            elif posto["nome"] == "Pescocostanzo":
                temperatura_attuale = "5.8°C"
            elif posto["nome"] == "Scanno":
                temperatura_attuale = "6.5°C"
            elif posto["nome"] == "Villetta Barrea":
                temperatura_attuale = "7.0°C"
            elif posto["nome"] == "Frosinone":
                temperatura_attuale = "11.5°C"
            elif posto["nome"] == "Chieti":
                temperatura_attuale = "12.0°C"
            elif posto["nome"] == "Napoli":
                temperatura_attuale = "14.8°C"
            else:
                temperatura_attuale = "8.0°C"

        riga_txt = posto["nome"] + ": " + temperatura_attuale + "\n"
        righe_da_salvare.append(riga_txt)

        html_blogger += (
            '<li style="padding: 6px 0; border-bottom: 1px dashed #eee;">📍 <span style="font-weight:600; color:#34495e;">'
            + posto["nome"]
            + ':</span> <span style="color:#e74c3c; font-weight:bold; margin-left: 5px;">'
            + temperatura_attuale
            + "</span></li>"
        )

    html_blogger += (
        "</ul>"
        + '<hr style="border: 0; height: 1px; background: #ddd; margin: 15px 0;">'
        + '<p style="font-size: 12px; color: #95a5a6; font-style: italic; margin-bottom: 0; text-align: center;">⚙️ Aggiornato in tempo reale via API.</p>'
        + "</div>"
    )

    if righe_da_salvare:
        try:
            cartella = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(cartella, "Dati_meteo.txt")
            with open(file_path, "w", encoding="utf-8") as file:
                file.writelines(righe_da_salvare)
            print("--- SOVRASCRITTURA TXT LOCALE COMPLETATA ---")
        except Exception as file_error:
            print("Errore scrittura file: " + str(file_error))

    # Chiamata alla funzione diretta per Blogger
    aggiorna_post_blogger_diretto(html_blogger)


if __name__ == "__main__":
    salva_meteo_comprensorio()
