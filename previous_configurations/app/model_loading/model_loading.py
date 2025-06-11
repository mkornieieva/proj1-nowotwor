from ultralytics import YOLO
import cv2
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'model2.0', 'weights', 'best.pt')

model = YOLO(MODEL_PATH)

def predict_and_draw(image_path):
    """
    Funkcja analizuje zdjęcie, rysuje wykryte zmiany (ramka + podpis "positive")
    lub napis "no detections", i zwraca obraz.
    """
    img = cv2.imread(image_path)
    results = model.predict(source=img, imgsz=640, conf=0.5)

    annotated_img = img.copy()

    boxes = results[0].boxes.xyxy.cpu().numpy()

    if len(boxes) == 0:
        print("No detections – dodawanie napisu na obraz.")
        # Dodaj napis na środku obrazu
        height, width = annotated_img.shape[:2]
        cv2.putText(annotated_img, 'no detections',
                    (width // 2 - 100, height // 2),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.0, (0, 0, 255), 2, cv2.LINE_AA)
    else:
        for box in boxes:
            x1, y1, x2, y2 = map(int, box)
            cv2.rectangle(annotated_img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(annotated_img, 'positive', (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    return annotated_img
