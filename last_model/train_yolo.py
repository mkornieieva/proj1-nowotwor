from ultralytics import YOLO

# ——— Użyj oficjalnego checkpointu zamiast uszkodzonego best.pt ———
MODEL     = r"C:\Users\USER\PycharmProjects\proj1-nowotwor\last_model\runs\detect_train_balanced\weights\best.pt"  # To pobierze i wczyta gotowy plik ~6 MB
DATA_YAML = r"C:\Users\USER\Downloads\dataset\data.yaml"

def main():
    # 1) Model zostanie pobrany, jeżeli go nie ma, i wczytany poprawnie
    model = YOLO(MODEL)

    # 2) Trening na zbalansowanym zbiorze
    model.train(
        data=DATA_YAML,
        epochs=20,
        imgsz=512,
        batch=8,
        device=0,
        hsv_h=0.015, hsv_s=0.7, hsv_v=0.4,
        mosaic=1.0, mixup=0.1,
        cls=1.0,
        cache=False,
        workers=0,
        project="runs", name="detect_train_balanced", exist_ok=True
    )

if __name__ == "__main__":
    main()
