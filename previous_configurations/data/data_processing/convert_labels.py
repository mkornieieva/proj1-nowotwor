import os

DIRECTORY = r"C:\Users\USER\Downloads\dataset\txt"

def process_annotation(file_path: str) -> None:
    """
    • usuwa dokładnie linię '0 0 0 0 0'
    • zmienia klasę 1 → 0
    • resztę zostawia bez zmian
    """
    new_lines = []
    with open(file_path, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line:
                continue
            parts = line.split()
            if len(parts) < 5:
                continue
            cls_id, coords = parts[0], parts[1:]
            if cls_id == "0" and coords == ["0", "0", "0", "0"]:
                continue            # odrzucamy „martwy” boks
            if cls_id == "1":
                cls_id = "0"
            new_lines.append(f"{cls_id} {' '.join(coords)}\n")

    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

def main() -> None:
    if not os.path.isdir(DIRECTORY):
        raise SystemExit(f"Invalid directory: {DIRECTORY}")

    for fname in os.listdir(DIRECTORY):
        if fname.lower().endswith(".txt"):
            path = os.path.join(DIRECTORY, fname)
            process_annotation(path)
            print(f"Processed {path}")

if __name__ == "__main__":
    main()
