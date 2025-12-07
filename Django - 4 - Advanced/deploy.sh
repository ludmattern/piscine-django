#!/bin/bash

echo -e "[0/4] Création du virtualenv..."
python3 -m venv .venv

echo -e "[1/4] Installation des dépendances..."
source .venv/bin/activate
pip install -r requirements.txt

echo -e "[2/4] Vérification de la connexion..."
python manage.py check

echo -e "[3/4] Application des migrations..."
python manage.py migrate

echo -e "[4/4] Lancement du serveur..."
python3 manage.py runserver
