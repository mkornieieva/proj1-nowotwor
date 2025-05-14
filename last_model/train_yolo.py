from ultralytics import YOLO

DATA_YAML = r"C:\Users\USER\Downloads\dataset\data.yaml"
MODEL     = r"C:\Users\USER\PycharmProjects\proj1-nowotwor\model\szkolenie_bez_zdrowych\0photos.pt"

def main():
    # Ładujemy istniejący checkpoint (Ultralytics‑format)
    model = YOLO(MODEL)

    # Jeśli chcesz kontynuować EXACT ten sam run:
    # last_model.train(resume=True)   # użyje hyper‑ i dat z checkpointu
    # ----- albo -----
    # Jeśli chcesz po prostu fine‑tune na nowych danych / innych hiperach:
    model.train(
        data=DATA_YAML,
        epochs=100,
        imgsz=512,
        batch=8,
        workers=0,
        cache=False,
        device=0,
        cls=1.0,
        hsv_h=0.015, hsv_s=0.7, hsv_v=0.4,
        mosaic=1.0, mixup=0.1,
        project="runs", name="detect_train", exist_ok=True
    )

if __name__ == "__main__":
    main()
