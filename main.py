import sys
import os
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QFileDialog, QSplitter, 
                             QLabel, QStackedWidget)
from PyQt6.QtSvgWidgets import QSvgWidget

# Importa il visualizzatore e il compilatore dal progetto originale
# (Assicurati che i path corrispondano alla struttura della repo)
from src.utils.stl_viewer import STLViewerWidget 
from src.utils.stl_compiler import STLCompilerWorker


class TileGeneratorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SVG to 3D Tile Generator")
        self.resize(1000, 600)

        self.current_svg = None
        self.current_stl = None

        self.init_ui()

    def init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        # Barra degli strumenti superiore
        toolbar_layout = QHBoxLayout()
        self.btn_import = QPushButton("Importa SVG")
        self.btn_export = QPushButton("Esporta STL")
        self.btn_export.setEnabled(False) # Disabilitato finché non c'è il modello
        
        self.btn_import.clicked.connect(self.import_svg)
        self.btn_export.clicked.connect(self.export_stl)

        toolbar_layout.addWidget(self.btn_import)
        toolbar_layout.addWidget(self.btn_export)
        toolbar_layout.addStretch()
        main_layout.addLayout(toolbar_layout)

        # Splitter per dividere lo schermo a metà
        splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(splitter)

        # --- PANNELLO SINISTRO: Visualizzatore SVG ---
        self.svg_viewer = QSvgWidget()
        self.svg_viewer.setMinimumWidth(400)
        splitter.addWidget(self.svg_viewer)

        # --- PANNELLO DESTRO: Stacked Widget (Loading / 3D Viewer) ---
        self.right_stack = QStackedWidget()
        
        # Pagina 1: Nessun modello
        self.lbl_empty = QLabel("Nessun modello caricato. Importa un SVG.")
        self.lbl_empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Pagina 2: Caricamento
        self.lbl_loading = QLabel("Generazione modello 3D in corso...\nAttendere prego.")
        self.lbl_loading.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_loading.setStyleSheet("font-weight: bold; color: blue;")
        
        # Pagina 3: Visualizzatore 3D
        self.stl_viewer = STLViewerWidget()

        self.right_stack.addWidget(self.lbl_empty)   # Index 0
        self.right_stack.addWidget(self.lbl_loading) # Index 1
        self.right_stack.addWidget(self.stl_viewer)  # Index 2

        splitter.addWidget(self.right_stack)
        splitter.setSizes([500, 500]) # Imposta le due metà uguali all'avvio

    def import_svg(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Importa Disegno SVG", "", "SVG Files (*.svg)")
        if file_path:
            self.current_svg = file_path
            self.svg_viewer.load(file_path)
            self.generate_3d_model()

    def generate_3d_model(self):
        self.right_stack.setCurrentIndex(1)
        self.btn_export.setEnabled(False)

        temp_stl = os.path.join(os.getcwd(), "temp_output.stl")

        self.compiler_thread = STLCompilerWorker(self.current_svg, temp_stl)
        
        # segnale 'progress' per aggiornare la UI
        # self.compiler_thread.progress.connect(self.update_loading_text)
        
        self.compiler_thread.finished.connect(self.on_model_ready)
        self.compiler_thread.error.connect(self.on_model_error)
        self.compiler_thread.start()

    def on_model_ready(self, stl_path):
        self.current_stl = stl_path
        
        # Qui dovrai dire al visualizzatore di caricare il nuovo STL
        self.stl_viewer.load_stl(stl_path)
        
        # Mostra il viewer 3D
        self.right_stack.setCurrentIndex(2)
        self.btn_export.setEnabled(True)

    def on_model_error(self, error_msg):
        self.lbl_empty.setText(f"Errore nella generazione:\n{error_msg}")
        self.right_stack.setCurrentIndex(0)

    def export_stl(self):
        if self.current_stl and os.path.exists(self.current_stl):
            save_path, _ = QFileDialog.getSaveFileName(self, "Esporta Modello STL", "tessera.stl", "STL Files (*.stl)")
            if save_path:
                import shutil
                shutil.copy(self.current_stl, save_path)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TileGeneratorApp()
    window.show()
    sys.exit(app.exec())