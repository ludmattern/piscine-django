#!/bin/bash

VENV_NAME="django_venv"

echo "Création du virtualenv $VENV_NAME..."
python3 -m venv $VENV_NAME

if [ ! -d "$VENV_NAME" ]; then
    echo "Erreur: Impossible de créer le virtualenv" >&2
    exit 1
fi

echo "Activation du virtualenv..."
source $VENV_NAME/bin/activate

echo "Mise à jour de pip..."
pip install --upgrade pip

echo "Installation des packages depuis requirement.txt..."
pip install -r requirement.txt

echo ""
echo "Packages installés:"
pip list

echo ""
echo "Le virtualenv $VENV_NAME est maintenant activé."
echo "Pour le désactiver, utilisez: deactivate"
