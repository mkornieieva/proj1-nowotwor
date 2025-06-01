from pathlib import Path
from ultralytics import YOLO
from sklearn.metrics import (
    confusion_matrix,
    classification_report,
    precision_recall_curve,
    roc_curve,
    auc
)
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import random

# ——— KONFIGURACJA ———
DATASET_DIR = Path(r"C:\Users\USER\Downloads\dataset\balanced")
MODEL_PATH  = Path(
    r"C:\Users\USER\PycharmProjects\proj1-nowotwor\last_model\runs\detect_train_balanced\weights\best.pt"
)
CONF_THRES  = 0.25      # próg decyzyjny slajd-level
MAX_IMAGES  = 10000     # maks. liczba testowanych obrazów

# Pliki wyjściowe
FIG_CM   = "confusion_matrix.png"
FIG_PR   = "PR_curve.png"
FIG_F1   = "F1_curve.png"
FIG_PREC = "P_curve.png"
FIG_REC  = "R_curve.png"
FIG_ROC  = "ROC_curve.png"   # nowy: krzywa ROC

# ——— Funkcje pomocnicze ———

def slide_gt(label_file: Path) -> int:
    """
    Zwraca 1, jeśli w .txt jest chociaż jedna niepusta linia (guz),
    w przeciwnym razie 0 (brak guza).
    """
    if not label_file.exists():
        return 0
    with open(label_file, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                return 1
    return 0


def slide_pred(model: YOLO, img: Path):
    """
    Zwraca tuple (pred_label, max_conf_score):
      - pred_label = 1, gdy znaleziono box o conf >= CONF_THRES
                    0 w przeciwnym razie
      - max_conf_score = najwyższa pewność spośród wykrytych boxów (lub 0.0)
    """
    # Najpierw wykrywamy boxy na bardzo niskim progu (0.001),
    # aby zebrać wszystkie predykcje. Potem sami porównamy conf z CONF_THRES
    res = model.predict(str(img), conf=0.001, save=False, verbose=False)
    boxes = res[0].boxes
    if len(boxes):
        max_conf = float(boxes.conf.max())
        pred_label = 1 if max_conf >= CONF_THRES else 0
        return pred_label, max_conf
    else:
        return 0, 0.0


def plot_confusion(cm: np.ndarray, path: str):
    """Rysuje i zapisuje macierz pomyłek 2×2."""
    plt.figure(figsize=(4, 3))
    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        cbar=False,
        xticklabels=["Pred+", "Pred-"],
        yticklabels=["True+", "True-"]
    )
    plt.title("Confusion Matrix")
    plt.tight_layout()
    plt.savefig(path, dpi=300)
    plt.close()


def plot_pr_curves(y_true, scores):
    """
    Rysuje i zapisuje wykresy:
      - Precision-Recall Curve
      - F1 vs Threshold
      - Precision vs Threshold
      - Recall vs Threshold
    """
    precision, recall, thresh = precision_recall_curve(y_true, scores)
    f1 = 2 * (precision * recall) / (precision + recall + 1e-9)

    # 1) Precision-Recall Curve
    plt.figure(figsize=(5, 4))
    plt.plot(recall, precision, linewidth=2)
    plt.xlabel("Recall")
    plt.ylabel("Precision")
    plt.title("Precision-Recall Curve")
    plt.grid(True, alpha=0.3)
    plt.savefig(FIG_PR, dpi=300)
    plt.close()

    # 2) F1 vs Threshold
    plt.figure(figsize=(5, 4))
    plt.plot(thresh, f1[:-1], linewidth=2)
    plt.xlabel("Confidence threshold")
    plt.ylabel("F1 score")
    plt.title("F1 vs Threshold")
    plt.grid(True, alpha=0.3)
    plt.savefig(FIG_F1, dpi=300)
    plt.close()

    # 3) Precision vs Threshold
    plt.figure(figsize=(5, 4))
    plt.plot(thresh, precision[:-1], linewidth=2)
    plt.xlabel("Confidence threshold")
    plt.ylabel("Precision")
    plt.title("Precision vs Threshold")
    plt.grid(True, alpha=0.3)
    plt.savefig(FIG_PREC, dpi=300)
    plt.close()

    # 4) Recall vs Threshold
    plt.figure(figsize=(5, 4))
    plt.plot(thresh, recall[:-1], linewidth=2)
    plt.xlabel("Confidence threshold")
    plt.ylabel("Recall")
    plt.title("Recall vs Threshold")
    plt.grid(True, alpha=0.3)
    plt.savefig(FIG_REC, dpi=300)
    plt.close()


def plot_roc_curve(y_true, scores, path: str):
    """
    Oblicza i rysuje krzywą ROC oraz wartość AUC.
    Zapisuje wynik do pliku 'path'.
    """
    fpr, tpr, thresh = roc_curve(y_true, scores)
    roc_auc = auc(fpr, tpr)

    plt.figure(figsize=(5, 4))
    plt.plot(fpr, tpr, color='darkorange', lw=2, label=f"AUC = {roc_auc:.3f}")
    plt.plot([0, 1], [0, 1], color='navy', lw=1, linestyle='--')
    plt.xlabel("False Positive Rate (FPR)")
    plt.ylabel("True Positive Rate (TPR)")
    plt.title("ROC Curve")
    plt.legend(loc="lower right")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(path, dpi=300)
    plt.close()


def main() -> None:
    # 1) Załaduj wytrenowany model
    model = YOLO(str(MODEL_PATH))

    # 2) Przygotuj listę obrazów z katalogu 'val'
    img_dir = DATASET_DIR / "images" / "val"
    lbl_dir = DATASET_DIR / "labels" / "val"

    img_paths = sorted(img_dir.glob("*.png"))
    if not img_paths:
        raise SystemExit(f"Brak plików .png w {img_dir}")

    # Ograniczenie do MAX_IMAGES (jeżeli jest ich więcej)
    if len(img_paths) > MAX_IMAGES:
        random.seed(42)
        img_paths = random.sample(img_paths, MAX_IMAGES)

    print(f"Testuję {len(img_paths)} obrazów z katalogu {img_dir}\n")

    # 3) Predykcje i etykiety
    y_true, y_pred, scores = [], [], []

    for img in img_paths:
        txt = lbl_dir / f"{img.stem}.txt"
        gt = slide_gt(txt)
        pred, score = slide_pred(model, img)

        y_true.append(gt)
        y_pred.append(pred)
        scores.append(score)

        print(f"{img.name:25s}  GT={gt}  PRED={pred}  score={score:.3f}")

    # 4) Macierz pomyłek i raport
    cm = confusion_matrix(y_true, y_pred, labels=[1, 0])
    tp, fn, fp, tn = cm.ravel()

    print("\nConfusion Matrix (slide-level):")
    print("           Pred+  Pred-")
    print(f"True +   {tp:6d} {fn:6d}")
    print(f"True -   {fp:6d} {tn:6d}")

    print("\nClassification report:")
    print(classification_report(y_true, y_pred, target_names=["no_tumor","tumor"]))

    # 5) Zapisz wykresy
    plot_confusion(cm, FIG_CM)
    plot_pr_curves(y_true, scores)
    plot_roc_curve(y_true, scores, FIG_ROC)

    print("\n📊  Zapisano wykresy:")
    for p in (FIG_CM, FIG_PR, FIG_F1, FIG_PREC, FIG_REC, FIG_ROC):
        print("   ", p)


if __name__ == "__main__":
    main()
