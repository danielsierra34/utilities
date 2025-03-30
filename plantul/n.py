import subprocess
import graphviz

def convertir_puml_a_imagen():
    archivo_puml = "plantuml.puml"
    archivo_dot = "diagrama.dot"
    
    # Generar archivo DOT usando PlantUML
    subprocess.run(["plantuml", "-graphvizdot", archivo_puml], check=True)

    # Leer el archivo DOT generado
    with open(archivo_dot, "r") as dot_file:
        dot_code = dot_file.read()
    
    # Generar imagen con Graphviz
    dot = graphviz.Source(dot_code)
    dot.render("diagrama", format="png", cleanup=True)
    print("Imagen generada: diagrama.png")

if __name__ == "__main__":
    convertir_puml_a_imagen()
