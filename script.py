import random
from datetime import datetime


def simulazione_meteo_roccaraso():
    orario_locale = datetime.now().strftime("%d/%m/%Y %H:%M")

    try:
        print("Generazione dati meteo locali per Roccaraso...")

        # Genera una temperatura casuale realistica tra -3.0°C e 12.0°C
        temperatura = round(random.uniform(-3.0, 12.0), 1)

        riga = f"[{orario_locale}] Roccaraso: {temperatura}°C (Dato Generato)\n"

        # Scrittura sul file mantenendo la D maiuscola
        with open("Dati_meteo.txt", "a", encoding="utf-8") as file:
            file.write(riga)

        print(f"-> SCRITTURA RIUSCITA: {riga.strip()}")

    except Exception as e:
        print(f"-> ERRORE CRITICO: {e}")


if __name__ == "__main__":
    simulazione_meteo_roccaraso()
