#!/bin/bash

# 0. Nettoyage (Optionnel)
rm db.sqlite3

echo -e "[1/5] Création de l'environnement virtuel..."
python3 -m venv .venv
source .venv/bin/activate

echo -e "[2/5] Installation des dépendances..."
pip install -r requirements.txt

echo -e "[3/5] Application des migrations..."
python3 manage.py migrate

echo -e "[4/5] Chargement des données (Fixtures)..."
python3 manage.py loaddata loremipsum/fixtures/data.json

echo -e "[5/5] Compilation des traductions..."
# Utilisation du script python car gettext n'est pas forcément installé sur le système
python3 compile_po.py

echo -e "Lancement du serveur..."
python3 manage.py runserver