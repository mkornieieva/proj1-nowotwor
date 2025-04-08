import os
import xml.etree.ElementTree as ET

def extract_bounding_boxes(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    image_width = int(root.find('size/width').text)
    image_height = int(root.find('size/height').text)

    bounding_boxes = []
    for obj in root.findall('object'):
        class_id = 0  # Assuming a single class, you can modify this as needed
        xmin = int(obj.find('bndbox/xmin').text)
        ymin = int(obj.find('bndbox/ymin').text)
        xmax = int(obj.find('bndbox/xmax').text)
        ymax = int(obj.find('bndbox/ymax').text)

        x_center = (xmin + xmax) / 2.0 / image_width
        y_center = (ymin + ymax) / 2.0 / image_height
        width = (xmax - xmin) / image_width
        height = (ymax - ymin) / image_height
        bounding_boxes.append(f"{class_id} {x_center} {y_center} {width} {height}")

    return bounding_boxes

def convert_xml_to_txt(xml_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for xml_file in os.listdir(xml_folder):
        if xml_file.endswith('.xml'):
            xml_path = os.path.join(xml_folder, xml_file)
            bounding_boxes = extract_bounding_boxes(xml_path)

            txt_file = os.path.splitext(xml_file)[0] + '.txt'
            txt_path = os.path.join(output_folder, txt_file)

            with open(txt_path, 'w') as f:
                for box in bounding_boxes:
                    f.write(box + '\n')

if __name__ == "__main__":
    xml_folder = r'E:\!!!!!STUDIAsem4\PROJ2\AI-detect\yolov5\dataset\labels\train-przed'  # Update with the path to your XML files
    output_folder = r'E:\!!!!!STUDIAsem4\PROJ2\AI-detect\yolov5\dataset\labels\train'  # Update with the path to save the TXT files
    convert_xml_to_txt(xml_folder, output_folder)