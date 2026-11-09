name: Scarica Meteo e Scrivi File

on:
  push:
    branches:
      - main
  schedule:
    - cron: '0 * * * *' # Esegue l'automazione ogni ora (opzionale)

jobs:
  crea-articolo:
    runs-on: ubuntu-latest

    steps:
    - name: Esamina il repository
      uses: actions/checkout@v4

    - name: Configura Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.10'

    - name: Installa le dipendenze
      run: |
        python -m pip install --upgrade pip
        pip install requests

    - name: Scarica Meteo e Scrivi File
      run: python script.py

    - name: Salva e pubblica i cambiamenti su Git
      run: |
        git config --local user.email "action@github.com"
        git config --local user.name "GitHub Action"
        git add meteo.txt
        # Esegue il commit solo se il file meteo.txt è effettivamente cambiato
        git diff --quiet && git diff --staged --quiet || (git commit -m "Aggiornato valore meteo" && git push)

