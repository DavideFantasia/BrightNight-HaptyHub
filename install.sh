#!/bin/bash

echo "================================================="
echo " Installazione di HaptyHub - BrightNight Edition "
echo "================================================="


# ==========================================
# CONTROLLO DIPENDENZE DI SISTEMA
# ==========================================

# Controllo OpenSCAD (necessario per la generazione 3D)
if ! command -v openscad &> /dev/null; then
    echo "OpenSCAD non trovato. Installazione in corso..."
    sudo apt-get update
    sudo apt-get install -y openscad
else
    echo "✔️ OpenSCAD è già installato."
fi
# ==========================================

# 1. Creazione dell'ambiente virtuale Python
echo "[1/3] Creazione dell'ambiente virtuale (venv)..."
python3 -m venv venv

# 2. Installazione delle dipendenze
echo "[2/3] Installazione delle librerie Python..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
deactivate

# Creazione file eseguibile per terminale
echo "[3/3] Creazione Eseguibile da Terminale..."
cat <<EOF > "run.sh"
#!/bin/bash
source venv/bin/activate
python main.py
deactivate
EOF
chmod +x "run.sh"

echo "========================================"
echo " Installazione Completata con successo! "
echo "========================================"
