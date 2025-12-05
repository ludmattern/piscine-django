#!/bin/bash

# Couleurs pour les messages
echo -e "[1/4] Démarrage de PostgreSQL..."
docker compose up -d

echo -e "[2/4] Création du virtualenv..."
python3 -m venv .venv

echo -e "[3/4] Installation des dépendances..."
source .venv/bin/activate
pip install -r requirements.txt > /dev/null 2>&1

echo -e "[4/4] Vérification de la connexion..."
python manage.py check

echo ""
echo -e "Prêt !"
echo "Pour activer le venv : source .venv/bin/activate"
echo "Pour lancer le serveur : python manage.py runserver"
