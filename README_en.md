[🇬🇧 Eng](README_en.md) | [🇮🇹 It](README.md)
---

# SVG to 3D Tile Generator

A Python and PyQt6 desktop application that transforms 2D vector drawings (SVG) into 3D tiles (STL) ready for printing. 

This project is a fork of [HaptyHub](https://github.com/DavideFantasia/HaptyHub) designed to showcase the main project at [BrightNight](https://bright-night.it/)@Pisa, isolating and highlighting its parametric generation and 3D visualization capabilities.

## Key Features

*   **Vector Import:** Load `.svg` files containing drawings and diagrams.
*   **Automatic Generation:** Dynamically creates an OpenSCAD script to extrude the drawing onto a predefined solid base.
*   **Integrated 3D Visualization:** Inspect the generated result directly within the app.
*   **Asynchronous Processing:** The user interface remains responsive during rendering thanks to background thread management.

## Prerequisites

To run the application, your system must meet the following requirements:
*   **Python 3.10+**
*   **OpenSCAD:** Must be installed and added to your operating system's `PATH` environment variable (the `openscad` command must work when launched from the terminal).

## Installation

1.  Clone the repository:
    ```bash
    git clone [https://github.com/DavideFantasia/BrightNight-HaptyHub](https://github.com/DavideFantasia/BrightNight-HaptyHub)
    cd BrightNight-HaptyHub
    ```
2.  Run the installation script for **Linux**:
    ```bash
    ./install.sh
    ```

## Usage

Launch the application from the terminal:
```bash
./run.sh
```
1. Click _Importa SVG_ to load your drawing.
2. Wait for the 3D model to be generated in the background.
3. Interact with the 3D viewer in the right panel.
4. Use _Esporta STL_ to save the model, ready to be sliced for 3D printing.

# SVG File Guidelines
To ensure OpenSCAD can successfully extrude the drawing, the SVG must follow these rules:
- It must be composed of closed paths and filled areas (fill).
- Avoid using simple lines (stroke) without first expanding or converting them into paths.
- Do not include embedded raster images (e.g., PNG/JPG) within the file.
