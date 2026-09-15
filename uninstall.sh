#!/bin/bash

echo "==========================================="
echo " Disinstallazione di HaptyGraph "
echo "==========================================="

# 1. Rimozione dell'Ambiente Virtuale
echo "[1/2] Rimozione dell'ambiente virtuale (venv)..."
if [ -d "venv" ]; then
    rm -rf venv
    echo "  -> Cartella venv rimossa."
else
    echo "  -> Cartella venv non trovata, salto."
fi

# 2. Rimozione dell'Eseguibile
echo "[2/2] Rimozione dell'eseguibile..."
if [ -f "run.sh" ]; then
    rm run.sh
    echo "  -> Eseguibile rimosso."
else
    echo "  -> Eseguibile non trovato, salto."
fi

echo "==========================================="
echo " Pulizia Completata con successo! "
echo " Ora puoi eliminare in sicurezza l'intera cartella del progetto."
echo "==========================================="
