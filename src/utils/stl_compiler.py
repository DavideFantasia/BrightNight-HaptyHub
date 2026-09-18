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
            
            # Modello OpenSCAD parametrico
            scad_content = f"""
            $fn = 32; // Risoluzione per le curve
            
            // Parametri della tessera
            width = 60;            
            length = 40;
            total_height = 3.5;    // Altezza totale del bordo esterno
            floor_height = 2.0;    // Altezza del pavimento interno (spessore della base)
            border_width = 2.0;    // Spessore del bordo rialzato (cornice)
            
            // L'estrusione del disegno parte dal pavimento e arriva esattamente a filo col bordo
            extrusion_height = total_height - floor_height; 
            
            // Parametri estetici
            r_corner = 4;          // Raggio degli angoli arrotondati
            bevel = 0.25;          // Smusso esterno
            
            // Modulo per creare il profilo 2D arrotondato
            module rounded_base(w, l, r) {{
                hull() {{
                    translate([w/2-r, l/2-r]) circle(r=r);
                    translate([-w/2+r, l/2-r]) circle(r=r);
                    translate([w/2-r, -l/2+r]) circle(r=r);
                    translate([-w/2+r, -l/2+r]) circle(r=r);
                }}
            }}

            union() {{
                difference() {{
                    // 1. Corpo principale alto (con smusso esterno)
                    minkowski() {{
                        linear_extrude(height = total_height - bevel)
                            rounded_base(width - bevel*2, length - bevel*2, max(0.1, r_corner - bevel));
                        
                        cylinder(r1=bevel, r2=0, h=bevel, $fn=16);
                    }}
                    
                    // 2. Scavo centrale (crea l'effetto a conca)
                    // Tagliamo la parte centrale partendo dall'altezza del pavimento verso l'alto
                    translate([0, 0, floor_height])
                    linear_extrude(height = total_height) {{
                        rounded_base(width - border_width*2, length - border_width*2, max(0.1, r_corner - border_width));
                    }}
                }}

                // 3. SVG estruso al centro
                // Inizia dal pavimento e si alza fino a raggiungere l'altezza del bordo
                translate([0, 0, floor_height])
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