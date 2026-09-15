[🇬🇧 Eng](README_en.md) | [🇮🇹 It](README.md)
# SVG to 3D Tile Generator

Applicazione desktop in Python e PyQt6 che trasforma disegni vettoriali 2D (SVG) in tessere 3D (STL) pronte per la stampa. 

Il progetto nasce come fork di (HaptyHub)[https://github.com/DavideFantasia/HaptyHub] con lo scopo di presentare il progetto principale alla (BrightNight)[https://bright-night.it/]@Pisa, isolando e mettendo in evidenza le funzionalità di generazione parametrica e visualizzazione 3D.

## Funzionalità Principali

*   **Importazione Vettoriale:** Carica file `.svg` contenenti disegni e schemi.
*   **Generazione Automatica:** Crea dinamicamente uno script OpenSCAD per estrudere il disegno su una base solida predefinita.
*   **Visualizzazione 3D Integrata:** Ispeziona il risultato generato direttamente nell'app.
*   **Elaborazione Asincrona:** L'interfaccia utente non si blocca durante il rendering, grazie alla gestione separata dei thread.

## Prerequisiti

Per eseguire correttamente l'applicazione, il tuo sistema deve soddisfare questi requisiti:
*   **Python 3.10+**
*   **OpenSCAD:** Deve essere installato e aggiunto alla variabile d'ambiente `PATH` del tuo sistema operativo (il comando `openscad` deve rispondere se lanciato da terminale).

## Installazione

1.  Clona la repository locale:
    ```bash
    git clone https://github.com/DavideFantasia/BrightNight-HaptyHub
    cd BrightNight-HaptyHub
    ```
2.  Avvia lo script di Installazione per **Linux**
3.  ```
    ./install.sh
    ```

## Utilizzo

Avvia l'applicazione dal terminale:
```bash
./run.sh
```
1. Clicca su _Importa SVG_ per caricare il disegno.
2. Attendi la generazione in background del modello.
3. Interagisci con il visualizzatore 3D nel pannello di destra.
4. Usa _Esporta STL_ per salvare il modello da dare in pasto al tuo slicer di fiducia.

# Linee Guida per i File SVG

Per far sì che OpenSCAD riesca a estrudere il disegno, l'SVG deve rispettare alcune regole:
-  Deve essere composto da tracciati chiusi e aree piene (fill).
-  Evitare l'uso di semplici linee (stroke) senza averle prima espanse/convertite in tracciati.
-  Non inserire immagini raster (es. PNG/JPG) incorporate nel file.
