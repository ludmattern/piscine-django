#!/bin/bash

echo -e "[1/5] Création de l'environnement virtuel..."
python3 -m venv .venv
source .venv/bin/activate

echo -e "[2/5] Installation des dépendances..."
pip install -r requirements.txt

echo -e "[3/5] Application des migrations..."
python3 manage.py migrate

echo -e "[4/5] Création des utilisateurs par défaut..."
python3 init.py

