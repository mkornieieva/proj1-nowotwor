from pathlib import Path
from ultralytics import YOLO
from sklearn.metrics import (confusion_matrix, classification_report,
                             precision_recall_curve)
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


DATASET_DIR = Path(r"C:\Users\USER\Downloads\dataset")          # główny katalog z png/ i txt/
MODEL_PATH  = Path(r"/last_model\runs\detect_train\weights\best.pt")
CONF_THRES  = 0.25   # domyślny próg slajd‑level
MAX_IMAGES  = 10000# limit testowanych obrazów

# nazwy plików wyjściowych
FIG_CM   = "confusion_matrix.png"
FIG_PR   = "PR_curve.png"
FIG_F1   = "F1_curve.png"
FIG_PREC = "P_curve.png"
FIG_REC  = "R_curve.png"


def slide_gt(label_file: Path) -> int:
    if not label_file.exists():
        return 0
    return 1 if any(line.strip() for line in label_file.open()) else 0


def slide_pred(model: YOLO, img: Path):
    """Zwraca tuple (label, conf_score):
    label  → 1 gdy ≥1 box (conf>=CONF_THRES) inaczej 0.
    conf_score → najwyższa pewność boxa lub 0 gdy brak boxów.
    """
    res = model.predict(str(img), conf=0.001, save=False, verbose=False)  # bardzo niski próg, żeby złapać score
    boxes = res[0].boxes
    if len(boxes):
        max_conf = float(boxes.conf.max())
        return (1 if max_conf >= CONF_THRES else 0), max_conf
    else:
        return 0, 0.0


def plot_confusion(cm: np.ndarray, path: str):
    plt.figure(figsize=(4, 3))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", cbar=False,
                xticklabels=["Pred+", "Pred-"], yticklabels=["True+", "True-"])
    plt.title("Confusion Matrix")
    plt.tight_layout()
    plt.savefig(path, dpi=300)
    plt.close()


def plot_pr_curves(y_true, scores):
    precision, recall, thresh = precision_recall_curve(y_true, scores)
    f1 = 2 * (precision * recall) / (precision + recall + 1e-9)

    # PR curve
    plt.figure()
    plt.plot(recall, precision)
    plt.xlabel("Recall")
    plt.ylabel("Precision")
    plt.title("Precision‑Recall Curve")
    plt.savefig(FIG_PR, dpi=300)
    plt.close()

    # F1 vs threshold
    plt.figure()
    plt.plot(thresh, f1[:-1])
    plt.xlabel("Confidence threshold")
    plt.ylabel("F1 score")
    plt.title("F1 vs Threshold")
    plt.savefig(FIG_F1, dpi=300)
    plt.close()

    # Precision vs threshold
    plt.figure()
    plt.plot(thresh, precision[:-1])
    plt.xlabel("Confidence threshold")
    plt.ylabel("Precision")
    plt.title("Precision vs Threshold")
    plt.savefig(FIG_PREC, dpi=300)
    plt.close()

    # Recall vs threshold
    plt.figure()
    plt.plot(thresh, recall[:-1])
    plt.xlabel("Confidence threshold")
    plt.ylabel("Recall")
    plt.title("Recall vs Threshold")
    plt.savefig(FIG_REC, dpi=300)
    plt.close()


def main() -> None:
    model = YOLO(str(MODEL_PATH))

    img_paths = sorted((DATASET_DIR / "png").glob("*.png"))
    if not img_paths:
        raise SystemExit("Brak plików .png w dataset/png")
    img_paths = img_paths[:MAX_IMAGES]

    y_true, y_pred, scores = [], [], []

    for img in img_paths:
        txt = DATASET_DIR / "txt" / f"{img.stem}.txt"
        gt   = slide_gt(txt)
        pred, score = slide_pred(model, img)
        y_true.append(gt)
        y_pred.append(pred)
        scores.append(score)
        print(f"{img.name:25s}  GT={gt}  PRED={pred}  score={score:.3f}")

    # confusion matrix & report
    cm = confusion_matrix(y_true, y_pred, labels=[1, 0])
    tp, fn, fp, tn = cm.ravel()

    print("\nConfusion Matrix (slide‑level):")
    print("           Pred+  Pred-")
    print(f"True +   {tp:6d} {fn:6d}")
    print(f"True -   {fp:6d} {tn:6d}")

    print("\nClassification report:")
    print(classification_report(y_true, y_pred, target_names=["no_tumor", "tumor"]))

    # save figures
    plot_confusion(cm, FIG_CM)
    plot_pr_curves(y_true, scores)
    print("\n📊  Zapisano wykresy:")
    for p in (FIG_CM, FIG_PR, FIG_F1, FIG_PREC, FIG_REC):
        print("   ", p)


if __name__ == "__main__":
    main()
