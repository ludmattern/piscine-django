#!/bin/bash

echo -e "[1/5] Création de l'environnement virtuel..."
python3 -m venv .venv
source .venv/bin/activate

echo -e "[2/5] Installation des dépendances..."
pip install -r requirements.txt