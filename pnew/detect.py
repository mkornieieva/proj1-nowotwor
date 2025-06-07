from ultralytics import YOLO
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR,'..', 'last_model', 'runs', 'detect_train_balanced', 'weights', 'best.pt')

model = YOLO(MODEL_PATH)

def detect_bounding_boxes_batch(image_paths):
    """
    Zwraca słownik: {ścieżka: [lista boxów]} dla wielu obrazów.
    """
    results = model.predict(source=image_paths, imgsz=640, conf=0.5)
    output = {}

    for img_path, result in zip(image_paths, results):
        boxes_raw = result.boxes.xyxy.cpu().numpy()
        bounding_boxes = []
        for box in boxes_raw:
            x1, y1, x2, y2 = map(int, box)
            bounding_boxes.append((x1, y1, x2 - x1, y2 - y1))
        output[img_path] = bounding_boxes

    return output