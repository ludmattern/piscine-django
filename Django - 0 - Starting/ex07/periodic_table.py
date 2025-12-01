#!/usr/bin/env python3

import sys


def parse_element(line):
    name, properties = line.strip().split(" = ")

    element = {"name": name}
    props = properties.split(", ")

    for prop in props:
        key, value = prop.split(":", 1)
        key = key.strip()
        value = value.strip()

        if key == "position" or key == "number":
            element[key] = int(value)
        else:
            element[key] = value

    return element


def read_periodic_table(filename):
    try:
        with open(filename, "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Erreur: fichier {filename} introuvable", file=sys.stderr)
        sys.exit(1)

    elements = []
    for line in lines:
        if line.strip():
            element = parse_element(line)
            elements.append(element)

    rows = []
    current_row = []

    for element in elements:
        position = element["position"]

        if position == 0 and current_row:
            rows.append(current_row)
            current_row = []

        current_row.append(element)

    if current_row:
        rows.append(current_row)

    return rows


def get_html_header():
    return """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tableau Périodique des Éléments</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            padding: 20px;
            background-color: #f5f5f5;
        }
        h1 {
            text-align: center;
            color: #333;
        }
        table {
            border-collapse: collapse;
            margin: 20px auto;
            background-color: white;
        }
        td {
            border: 1px solid black;
            padding: 5px;
            width: 80px;
            height: 100px;
            position: relative;
            background-color: #e8f4f8;
        }
        td.empty {
            border: none;
            background-color: transparent;
        }
        .atomic-number {
            position: absolute;
            top: 5px;
            left: 5px;
            font-size: 12px;
            font-weight: bold;
            color: #2c3e50;
        }
        .symbol {
            font-size: 36px;
            font-weight: bold;
            color: #2c3e50;
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
        }
        .name {
            position: absolute;
            bottom: 5px;
            left: 50%;
            transform: translateX(-50%);
            font-size: 11px;
            color: #555;
        }
        .molecular-weight {
            position: absolute;
            top: 5px;
            right: 5px;
            font-size: 10px;
            color: #666;
        }
        ul.element-info {
            list-style-type: none;
        }
    </style>
</head>
<body>
    <h1>Tableau Périodique des Éléments</h1>
    <table>
"""


def get_html_footer():
    return """    </table>
</body>
</html>
"""


def format_electron_text(electron_config):
    electron_parts = electron_config.split()
    if not electron_parts:
        return "0 electrons"
    if len(electron_parts) == 1:
        return f"{electron_config} electron"
    else:
        return f"{electron_config} electrons"


def generate_element_cell(element):
    """Génère le HTML pour une cellule d'élément."""
    return f"""            <td>
                <ul class="element-info">
                    <li class="atomic-number">{element["number"]}</li>
                    <li class="symbol">{element["small"]}</li>
                    <li class="molecular-weight">{element["molar"]}</li>
                    <li class="name"><h4>{element["name"]}</h4></li>
                </ul>
            </td>
"""


def generate_table_row(row):
    html = "        <tr>\n"

    cells = [None] * 18
    for element in row:
        position = element["position"]
        cells[position] = element

    for cell in cells:
        if cell is None:
            html += '            <td class="empty"></td>\n'
        else:
            html += generate_element_cell(cell)

    html += "        </tr>\n"
    return html


def generate_html(rows, output_filename):
    html = get_html_header()

    for row in rows:
        html += generate_table_row(row)

    html += get_html_footer()

    with open(output_filename, "w") as f:
        f.write(html)

    print(f"Fichier {output_filename} généré avec succès!")


def main():
    input_file = "periodic_table.txt"
    output_file = "periodic_table.html"

    rows = read_periodic_table(input_file)
    generate_html(rows, output_file)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Erreur: {e}", file=sys.stderr)
        sys.exit(1)
