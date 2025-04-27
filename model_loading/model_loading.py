from ultralytics import YOLO
import cv2
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'model2.0', 'weights', 'best.pt')

model = YOLO(MODEL_PATH)

def predict_and_draw(image_path):
    """
    Funkcja analizuje zdjęcie, rysuje wykryte zmiany (ramka + podpis "positive") i zwraca obraz.
    """
    img = cv2.imread(image_path)
    results = model.predict(source=img, imgsz=640, conf=0.5)

    annotated_img = img.copy()

    for box in results[0].boxes.xyxy.cpu().numpy():
        x1, y1, x2, y2 = map(int, box)

        # Rysujemy prostokąt (zielona ramka)
        cv2.rectangle(annotated_img, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Podpis "positive" nad ramką
        cv2.putText(annotated_img, 'positive', (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    return annotated_img
