
            // Parametri della tessera
            width = 50;
            length = 50;
            base_thickness = 2;
            extrusion_height = 1.5;

            // Generazione del solido
            union() {
                // Base solida
                cube([width, length, base_thickness], center=true);
                
                // SVG estruso in superficie
                translate([0, 0, base_thickness/2])
                linear_extrude(height = extrusion_height) {
                    import("/home/davide/Applicazioni/BrightNight-HaptyHub/input/nuvola.svg", center=true);
                }
            }
            