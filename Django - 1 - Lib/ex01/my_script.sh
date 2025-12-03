#!/bin/bash

pip --version

INSTALL_DIR="local_lib"
LOG_FILE="install.log"

if [ -d "$INSTALL_DIR" ]; then
    echo "Suppression de l'ancienne installation..."
    rm -rf "$INSTALL_DIR"
fi

mkdir -p "$INSTALL_DIR"
echo "Installation de path.py depuis GitHub..."
pip install --upgrade --target="$INSTALL_DIR" --force-reinstall git+https://github.com/jaraco/path.git > "$LOG_FILE" 2>&1

if [ $? -eq 0 ]; then
    echo "Installation réussie, exécution de my_program.py..."
    python3 my_program.py
else
    echo "Erreur lors de l'installation. Consultez $LOG_FILE pour plus de détails."
    exit 1
fi
