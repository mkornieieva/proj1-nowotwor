import os
import numpy as np
from xml.etree import ElementTree


def get_category(category_file):
    """
    Odczytuje plik tekstowy z kategoriami (jedna nazwa w linii) i zwraca listę kategorii.
    """
    class_list = []
    with open(category_file, 'r') as f:
        for line in f.readlines():
            class_list.append(line.strip())
    print("Załadowane kategorie:", class_list)
    return class_list


def _to_one_hot(name, num_classes):
    """
    Konwertuje nazwę klasy (np. 'A', 'B', 'E', 'G') na wektor one-hot.
    Przyjmujemy, że mamy num_classes elementów.
    """
    one_hot_vector = [0] * num_classes
    if name == 'A':
        one_hot_vector[0] = 1
    elif name == 'B':
        one_hot_vector[1] = 1
    elif name == 'E':
        one_hot_vector[2] = 1
    elif name == 'G':
        one_hot_vector[3] = 1
    else:
        print('Nieznana etykieta:', name)
    return one_hot_vector


def process_annotation_file(xml_file, num_classes, normalize=True):
    """
    Przetwarza pojedynczy plik XML z adnotacjami.
    Pobiera:
      - wymiary obrazu (width, height)
      - nazwę obrazu (z elementu <filename>) – to będzie nazwa pliku DICOM,
      - dla każdego obiektu: współrzędne bounding boxa oraz nazwę klasy, którą koduje do one-hot.
    Zwraca krotkę (image_name, annotations).
    Jeśli normalize=True, współrzędne są dzielone przez width i height.
    """
    print("Przetwarzam plik XML:", xml_file)
    tree = ElementTree.parse(xml_file)
    root = tree.getroot()

    # Pobierz wymiary obrazu
    size_elem = root.find('size')
    width = float(size_elem.find('width').text)
    height = float(size_elem.find('height').text)
    print("Wymiary obrazu:", width, "x", height)

    # Pobierz nazwę obrazu z elementu <filename>, jeśli istnieje; w przeciwnym razie użyj nazwy pliku XML.
    filename_elem = root.find('filename')
    if filename_elem is not None:
        image_name = filename_elem.text.strip()
    else:
        image_name = os.path.splitext(os.path.basename(xml_file))[0]
    print("Nazwa obrazu:", image_name)

    objects = root.findall('object')
    print("Liczba obiektów w pliku XML:", len(objects))

    bounding_boxes = []
    one_hot_classes = []
    for obj in objects:
        bndbox = obj.find('bndbox')
        if bndbox is None:
            print("Brak tagu <bndbox> w obiekcie.")
            continue
        if normalize:
            xmin = float(bndbox.find('xmin').text) / width
            ymin = float(bndbox.find('ymin').text) / height
            xmax = float(bndbox.find('xmax').text) / width
            ymax = float(bndbox.find('ymax').text) / height
        else:
            xmin = float(bndbox.find('xmin').text)
            ymin = float(bndbox.find('ymin').text)
            xmax = float(bndbox.find('xmax').text)
            ymax = float(bndbox.find('ymax').text)
        bounding_boxes.append([xmin, ymin, xmax, ymax])

        class_name = obj.find('name').text.strip()
        one_hot = _to_one_hot(class_name, num_classes)
        one_hot_classes.append(one_hot)

    if len(bounding_boxes) == 0:
        print("Brak adnotacji (bounding boxes) w pliku:", xml_file)

    bounding_boxes = np.array(bounding_boxes)
    one_hot_classes = np.array(one_hot_classes)
    annotations = np.hstack((bounding_boxes, one_hot_classes))
    print("Kształt macierzy adnotacji:", annotations.shape)
    return image_name, annotations


def one_hot_to_class(one_hot_vector):
    """
    Konwertuje wektor one-hot do numeru klasy (indeks, w którym znajduje się 1).
    """
    return int(np.argmax(one_hot_vector))


def convert_bbox_to_yolo(bbox, width, height):
    """
    Konwertuje współrzędne bounding boxa z formatu [xmin, ymin, xmax, ymax]
    na format YOLO: (x_center, y_center, width, height) – wartości znormalizowane względem wymiarów obrazu.
    """
    xmin, ymin, xmax, ymax = bbox
    x_center = (xmin + xmax) / 2.0 / width
    y_center = (ymin + ymax) / 2.0 / height
    box_width = (xmax - xmin) / width
    box_height = (ymax - ymin) / height
    return x_center, y_center, box_width, box_height


def save_annotations_to_txt(image_name, annotations, output_dir, width, height):
    """
    Zapisuje adnotacje do pliku TXT w formacie YOLO.
    Nazwa pliku TXT odpowiada nazwie obrazu (bez rozszerzenia) i zostaje zapisana w folderze output_dir.
    Każdy wiersz ma format:
       <Class_ID> <x_center> <y_center> <width> <height>
    """
    base_name = os.path.splitext(image_name)[0]
    output_file = os.path.join(output_dir, base_name + '.txt')
    with open(output_file, 'w') as f:
        for row in annotations:
            bbox = row[:4]
            one_hot = row[4:]
            class_id = one_hot_to_class(one_hot)
            x_center, y_center, box_width, box_height = convert_bbox_to_yolo(bbox, width, height)
            f.write(f"{class_id} {x_center:.6f} {y_center:.6f} {box_width:.6f} {box_height:.6f}\n")
    print("Zapisano adnotacje do:", output_file)


def process_all_annotations(annotation_dir, output_dir, num_classes, normalize=True, category_file='category.txt'):
    """
    Przetwarza wszystkie pliki XML z adnotacjami znajdujące się w katalogu annotation_dir.
    Funkcja przeszukuje folder rekurencyjnie, aby znaleźć wszystkie pliki XML.
    Dla każdego pliku:
      - przetwarza adnotacje,
      - zapisuje plik TXT z danymi numerycznymi.
    Nazwa pliku TXT odpowiada nazwie pliku DICOM, pobieranej z elementu <filename> w XML.
    """
    os.makedirs(output_dir, exist_ok=True)
    for root_dir, subdirs, files in os.walk(annotation_dir):
        print("Przeszukuję katalog:", root_dir)
        for filename in files:
            if not filename.endswith('.xml'):
                continue
            xml_path = os.path.join(root_dir, filename)
            try:
                image_name, annotations = process_annotation_file(xml_path, num_classes, normalize)
                tree = ElementTree.parse(xml_path)
                root_elem = tree.getroot()
                size_elem = root_elem.find('size')
                image_width = float(size_elem.find('width').text)
                image_height = float(size_elem.find('height').text)
                save_annotations_to_txt(image_name, annotations, output_dir, image_width, image_height)
            except Exception as e:
                print(f"Błąd przetwarzania pliku {filename}: {e}")


if __name__ == '__main__':
    # Ustaw ścieżki – używaj surowych łańcuchów (r'...') dla Windows
    annotation_directory = r'C:\Users\zosia\OneDrive\Documents\10 I Rok Telco\04 Sem 4\pluco1\pythonProject8\Annotation'
    output_directory = r'C:\Users\zosia\OneDrive\Documents\10 I Rok Telco\04 Sem 4\pluco1\pythonProject8\YOLO_annotations'
    num_classes = 4  # np. dla 'A', 'B', 'E', 'G'

    process_all_annotations(annotation_directory, output_directory, num_classes, normalize=True)
