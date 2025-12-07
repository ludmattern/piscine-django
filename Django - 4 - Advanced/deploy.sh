#!/bin/bash

echo -e "[0/6] Recréation des containers existants..."
docker compose down
docker compose up -d

echo -e "[1/6] Démarrage de PostgreSQL..."
docker compose up -d

echo -e "[2/6] Création du virtualenv..."
python3 -m venv .venv

echo -e "[3/6] Installation des dépendances..."
source .venv/bin/activate
pip install -r requirements.txt

echo -e "[4/6] Vérification de la connexion..."
python manage.py check

echo -e "[5/6] Application des migrations..."
python manage.py migrate

echo -e "[6/6] Lancement du serveur..."
python3 manage.py runserver
