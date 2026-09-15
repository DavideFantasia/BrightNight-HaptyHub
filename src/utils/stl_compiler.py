from PyQt6.QtCore import QThread, pyqtSignal
import os, subprocess

class STLCompilerWorker(QThread):
    progress = pyqtSignal(str)
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, svg_path, output_stl_path):
        """
        :param svg_path: Il percorso assoluto del file SVG da estrudere.
        :param output_stl_path: Il percorso dove salvare il file STL finale.
        """
        super().__init__()
        self.svg_path = svg_path
        self.output_stl_path = output_stl_path

    def run(self):
        try:
            self.progress.emit("Generazione script OpenSCAD in corso...")
            
            # 1. Normalizza il path dell'SVG. 
            # OpenSCAD preferisce gli slash in avanti (/), anche su Windows, 
            # altrimenti la funzione import() potrebbe fallire.
            safe_svg_path = os.path.abspath(self.svg_path).replace('\\', '/')
            
            # Assicuriamoci che la cartella di output esista
            output_dir = os.path.dirname(os.path.abspath(self.output_stl_path))
            os.makedirs(output_dir, exist_ok=True)
            
            # 2. Crea il file SCAD temporaneo
            temp_scad_path = os.path.join(output_dir, "temp_tile.scad")
            
            # Modello OpenSCAD parametrico generato dinamicamente
            scad_content = f"""
            // Parametri della tessera
            width = 50;
            length = 50;
            base_thickness = 2;
            extrusion_height = 1.5;

            // Generazione del solido
            union() {{
                // Base solida
                cube([width, length, base_thickness], center=true);
                
                // SVG estruso in superficie
                translate([0, 0, base_thickness/2])
                linear_extrude(height = extrusion_height) {{
                    import("{safe_svg_path}", center=true);
                }}
            }}
            """
            
            with open(temp_scad_path, "w") as f:
                f.write(scad_content)

            # 3. Compilazione in STL
            self.progress.emit("Compilazione con OpenSCAD... Potrebbe richiedere qualche secondo.")
            
            # Lanciamo il subprocess di OpenSCAD
            cmd_scad = ["openscad", "-o", self.output_stl_path, temp_scad_path]
            
            # capture_output=True ci permette di leggere gli errori se OpenSCAD fallisce
            process = subprocess.run(cmd_scad, check=True, text=True, capture_output=True)

            # 4. Successo! Invia il path generato alla UI
            self.finished.emit(self.output_stl_path)

        except subprocess.CalledProcessError as e:
            # Se OpenSCAD fallisce (es. SVG malformato), catturiamo lo stderr
            self.error.emit(f"Errore di OpenSCAD:\n{e.stderr}")
        except Exception as e:
            self.error.emit(str(e))