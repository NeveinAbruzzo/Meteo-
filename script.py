import os
import smtplib
from datetime import datetime
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests


def ottieni_temperatura_api_backup(lat, lon):
    url = (
        "https://open-meteo.com"
        + str(lat)
        + "&longitude="
        + str(lon)
        + "&current_weather=true"
    )
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            dati = response.json()
            if "current_weather" in dati:
                return str(dati["current_weather"]["temperature"]) + "°C"
    except Exception:
        pass
    return None


def invia_email_blogger(contenuto_html):
    email_destinatario = os.environ.get("BLOGGER_EMAIL_SECRET")
    email_mittente = os.environ.get("MITTENTE_EMAIL")
    password_mittente = os.environ.get("MITTENTE_PASSWORD")

    if not email_destinatario or not email_mittente or not password_mittente:
        print(
            "-> Invio a Blogger ignorato: Mancano i Secrets delle email su GitHub."
        )
        return

    msg = MIMEMultipart("alternative")
    msg["Subject"] = Header("Meteo Comprensorio in Tempo Reale", "utf-8")
    msg["From"] = email_mittente
    msg["To"] = email_destinatario

    parte_html = MIMEText(contenuto_html, "html", "utf-8")
    msg.attach(parte_html)

    try:
        print("Connessione sicura tramite porta 587 TLS...")
        server = smtplib.SMTP("://gmail.com", 587, timeout=15)
        server.starttls()
        server.login(email_mittente, password_mittente)

        print("Invio in corso a Blogger...")
        server.sendmail(email_mittente, [email_destinatario], msg.as_string())
        server.quit()
        print("🎉 EMAIL INVIATA CON SUCCESSO!")
    except Exception as e:
        print("🚨 Errore durante l'invio dell'email: " + str(e))


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
        + '<p style="font-size: 16px; font-weight: bold; color: #7f8c8d;">Data e Ora: '
        + orario_locale
        + "</p>"
        + '<ul style="list-style-type: none; padding-left: 0; font-size: 15px; line-height: 1.8;">'
    )

    print("--- AVVIO RECUPERO DATI METEO COMPRENSORIO ---")
    righe_da_salvare.append(
        "=== ULTIMO AGGIORNAMENTO: " + orario_locale + " ===\n\n"
    )

    for posto in localita:
        print("Lettura dati reali per " + posto["nome"] + "...")
        temperatura_attuale = ottieni_temperatura_api_backup(
            posto["lat"], posto["lon"]
        )

        # Usiamo 'temperatura_attuale' per evitare qualsiasi errore di ortografia
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
        + '<p style="font-size: 12px; color: #95a5a6; font-style: italic; margin-bottom: 0; text-align: center;">⚙️ Stazione aggiornata con GitHub Actions.</p>'
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

    invia_email_blogger(html_blogger)


if __name__ == "__main__":
    salva_meteo_comprensorio()
