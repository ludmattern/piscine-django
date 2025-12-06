echo -e "[0/1] Création du virtualenv..."
python3 -m venv .venv

echo -e "[1/1] Installation des dépendances..."
source .venv/bin/activate
pip install -r requirements.txt