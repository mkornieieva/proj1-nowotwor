from PIL import Image
import os


#ścieżki do zmiany
extract_path = r"C:\Users\klaud\Downloads\extracted_data_fixed"
output_path = r"C:\Users\klaud\Downloads\processed_data_final"


# Dane do połączenia z bazą
DB_USER = "nowotwor_user"
DB_PASSWORD = "nowotwor_eiti"
DB_DSN = "localhost/XEPDB1"

def get_db_connection():
    return cx_Oracle.connect(DB_USER, DB_PASSWORD, DB_DSN)


if not os.path.exists(output_path):
    os.makedirs(output_path)

TARGET_SIZE = (256, 256)

for root, dirs, files in os.walk(extract_path):
    for file in files:
        if file.endswith((".png", ".jpg", ".jpeg")):
            image_path = os.path.join(root, file)

            try:
                with Image.open(image_path) as img:
                    img_resized = img.resize(TARGET_SIZE, Image.Resampling.LANCZOS)


                    relative_path = os.path.relpath(root, extract_path)
                    save_dir = os.path.join(output_path, relative_path)
                    if not os.path.exists(save_dir):
                        os.makedirs(save_dir)

                    save_path = os.path.join(save_dir, file)
                    img_resized.save(save_path)
            except Exception as e:
                print(f"Błąd podczas przetwarzania zdjęcia {image_path}: {e}")

print("Koniec. Obrazy zapisano w:", output_path)