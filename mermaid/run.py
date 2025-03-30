import os
import re
import sys

def sanitize_id(name):
    """Convierte el nombre en un identificador válido para Mermaid."""
    clean_name = re.sub(r"[^a-zA-Z0-9_]", "_", name)
    if re.match(r"^\d", clean_name):  # Si empieza con un número, agrega prefijo "ID_"
        clean_name = "ID_" + clean_name
    return clean_name

def clean_name(name):
    """Elimina cualquier prefijo antes de '- ' incluyendo el propio '- '."""
    return re.sub(r".*-\s*", "", name)

def generate_mermaid(output_file, orientacion="LR"):
    directory = "navigation"
    mermaid_lines = [f"graph {orientacion};"]  # Dirección de izquierda a derecha
    node_map = {}  # Mapea los nodos existentes
    base_url = f"https://storage.googleapis.com/pruebasautomatizadas-ghost/"

    for root, dirs, files in os.walk(directory):
        relative_path = os.path.relpath(root, directory)
        path_parts = relative_path.split(os.sep) if relative_path != "." else []
        
        parent_node = sanitize_id(directory)  # Nodo raíz
        if parent_node not in node_map:
            node_map[parent_node] = f'{parent_node}["{clean_name(directory)}"]:::transparentNode'
            mermaid_lines.append(node_map[parent_node])

        # Identificar imágenes en la carpeta
        images = {os.path.splitext(clean_name(f))[0]: f for f in files if f.lower().endswith(".png")}

        # Crear nodos para carpetas
        for part in path_parts:
            clean_part = clean_name(part)
            node_id = sanitize_id(clean_part)

            if node_id not in node_map:
                # Si hay una imagen PNG con el mismo nombre, agregarla
                img_tag = ""
                if clean_part in images:
                    image_url = base_url + relative_path.replace(os.sep, "/") + "/" + images[clean_part]
                    img_tag = f'<br/><img src="{image_url}" width="100"/>'

                node_map[node_id] = f'{node_id}["{clean_part}{img_tag}"]:::transparentNode'
                mermaid_lines.append(node_map[node_id])
                mermaid_lines.append(f"{parent_node} --> {node_id}")

            parent_node = node_id  # Establecer el nodo padre

        # Agrupar archivos y fusionar nodos duplicados
        file_groups = {}
        for file in files:
            clean_file_name = clean_name(file)
            file_name_no_ext = os.path.splitext(clean_file_name)[0]  # Nombre sin extensión
            if file_name_no_ext not in file_groups:
                file_groups[file_name_no_ext] = {"files": [], "image": None}
            file_groups[file_name_no_ext]["files"].append(file)
            if file.lower().endswith(".png"):
                file_groups[file_name_no_ext]["image"] = file  # Guardar la imagen

        for file_name_no_ext, data in file_groups.items():
            node_id = sanitize_id(file_name_no_ext)

            if node_id in node_map and data["image"]:
                # Si ya existe el nodo sin imagen, agrégale la imagen
                image_url = base_url + relative_path.replace(os.sep, "/") + "/" + data["image"]
                node_map[node_id] = f'{node_id}["{file_name_no_ext}<br/><img src=\'{image_url}\' width=\'100\'/>"]:::transparentNode'
                mermaid_lines = [line if not line.startswith(f"{node_id}[") else node_map[node_id] for line in mermaid_lines]
                mermaid_lines.append(f'click {node_id} "{image_url}"')
            elif node_id not in node_map:
                # Crear nuevo nodo si no existe aún
                if data["image"]:
                    image_url = base_url + relative_path.replace(os.sep, "/") + "/" + data["image"]
                    node_map[node_id] = f'{node_id}["{file_name_no_ext}<br/><img src=\'{image_url}\' width=\'100\'/>"]:::transparentNode'
                    mermaid_lines.append(node_map[node_id])
                    mermaid_lines.append(f'click {node_id} "{image_url}"')
                else:
                    node_map[node_id] = f'{node_id}["{file_name_no_ext}"]:::transparentNode'
                    mermaid_lines.append(node_map[node_id])

            mermaid_lines.append(f"{parent_node} --> {node_id}")

    # Definir el estilo para nodos transparentes
    mermaid_lines.append('classDef transparentNode fill:#2d2d2d,color:white,stroke:#333,stroke-width:2px,rx:10,ry:10;')

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(mermaid_lines))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python script.py <orientacion>")
        sys.exit(1)
    
    orientacion = sys.argv[1]
    generate_mermaid("mermaid.mmd", orientacion)
