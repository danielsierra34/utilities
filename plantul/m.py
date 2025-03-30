import json

def json_to_plantuml(json_data):
    """Convierte un JSON en una notación de PlantUML"""
    plantuml_code = "@startuml\n"
    
    def parse_dict(d, parent=None):
        for key, value in d.items():
            node = f"{key}"
            if parent:
                plantuml_code_list.append(f"{parent} --> {node}")
            if isinstance(value, dict):
                parse_dict(value, node)
            elif isinstance(value, list):
                for i, item in enumerate(value):
                    list_node = f"{node}_{i}"
                    plantuml_code_list.append(f"{node} --> {list_node}")
                    if isinstance(item, dict):
                        parse_dict(item, list_node)
                    else:
                        plantuml_code_list.append(f"{list_node} : {item}")
            else:
                plantuml_code_list.append(f"{node} : {value}")
    
    plantuml_code_list = []
    parse_dict(json_data)
    plantuml_code += "\n".join(plantuml_code_list)
    plantuml_code += "\n@enduml"
    return plantuml_code


def save_plantuml_file(plantuml_code, filename="plantuml.puml"):
    with open(filename, "w") as f:
        f.write(plantuml_code)
    return filename


def read_json_file(filename="db.json"):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)


if __name__ == "__main__":
    json_data = read_json_file("db.json")
    plantuml_code = json_to_plantuml(json_data)
    puml_file = save_plantuml_file(plantuml_code)
    print(f"PlantUML generado en {puml_file}")
