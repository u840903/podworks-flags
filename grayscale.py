import os
import re
import xml.etree.ElementTree as ET

def rgb_to_grayscale(hex_color):
    # Convert hex to RGB
    hex_color = hex_color.lstrip('#')
    r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    # Compute grayscale value
    gray = int(0.299 * r + 0.587 * g + 0.114 * b)
    # Convert grayscale value back to hex
    gray_hex = f'#{gray:02x}{gray:02x}{gray:02x}'
    return gray_hex

def process_svg_file(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        # Namespace handling
        namespaces = {'svg': 'http://www.w3.org/2000/svg'}

        for elem in root.findall('.//*[@fill]', namespaces):
            fill_color = elem.attrib['fill']
            if re.match(r'^#([A-Fa-f0-9]{6})$', fill_color):
                grayscale_color = rgb_to_grayscale(fill_color)
                elem.set('fill', grayscale_color)

        tree.write(file_path, xml_declaration=True, encoding='utf-8')
        print(f"Processed file: {file_path}")
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")

def process_all_svgs_in_folder(folder_path):
    if not os.path.exists(folder_path):
        print(f"Directory {folder_path} does not exist.")
        return

    for filename in os.listdir(folder_path):
        if filename.endswith('.svg'):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                process_svg_file(file_path)
            else:
                print(f"File {file_path} does not exist.")

# Replace './flags' with the actual path to the folder containing the SVG files
process_all_svgs_in_folder('./flags')
