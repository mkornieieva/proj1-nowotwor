# -------- split_dataset.py --------
import random, shutil
from pathlib import Path

ROOT = Path(r"C:\Users\USER\Downloads\dataset")
N_TRAIN, N_VAL = 10000, 2500
png_all = sorted((ROOT / "png").glob("*.png"))
assert len(png_all) >= N_TRAIN + N_VAL, "Za mało obrazów w png/"

random.shuffle(png_all)
train_imgs = png_all[:N_TRAIN]
val_imgs   = png_all[N_TRAIN:N_TRAIN + N_VAL]

def copy_subset(img_paths, subset):
    for img in img_paths:
        lbl = ROOT / "txt" / f"{img.stem}.txt"
        # dest:
        (ROOT / "images" / subset).mkdir(parents=True, exist_ok=True)
        (ROOT / "labels" / subset).mkdir(parents=True, exist_ok=True)
        shutil.copy2(img, ROOT / "images" / subset / img.name)
        shutil.copy2(lbl, ROOT / "labels" / subset / f"{img.stem}.txt")

copy_subset(train_imgs, "train")
copy_subset(val_imgs,   "val")
print(f"➡  skopiowano {len(train_imgs)} train  +  {len(val_imgs)} val")



###bash python split_dataset.py
