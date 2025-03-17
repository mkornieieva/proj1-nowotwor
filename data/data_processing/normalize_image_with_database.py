import os
import cx_Oracle  # biblioteka do połączenia z Oracle
from PIL import Image
from io import BytesIO

# Dane do połączenia z bazą
DB_USER = "nowotwor_user"
DB_PASSWORD = "nowotwor_eiti"
DB_DSN = "localhost/XEPDB1"


# Funkcja do łączenia się z bazą
def get_db_connection():
    return cx_Oracle.connect(DB_USER, DB_PASSWORD, DB_DSN)


# Funkcja do pobrania obrazu z bazy
def get_image_from_db(image_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Pobranie obrazu jako BLOB
    cursor.execute("SELECT image_data FROM data WHERE id = :id", {"id": image_id})
    row = cursor.fetchone()

    cursor.close()
    conn.close()

    if row and row[0]:
        return Image.open(BytesIO(row[0].read()))  # Konwersja BLOB -> Image
    else:
        return None


# Funkcja do zapisania przetworzonego obrazu w bazie
def save_processed_image(image_id, processed_image):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Konwersja Image -> BLOB
    img_byte_arr = BytesIO()
    processed_image.save(img_byte_arr, format="JPEG")
    img_byte_arr = img_byte_arr.getvalue()

    # Wstawienie do tabeli ProcessedImages
    cursor.execute("""
        INSERT INTO ProcessedImages (proc_image_id, id, filename, image_data, processing_date) 
        VALUES (SEQ_PROCESSED_IMG_ID.NEXTVAL, :id, :filename, :image_data, SYSTIMESTAMP)
    """, {"id": image_id, "filename": f"processed_{image_id}.jpg", "image_data": img_byte_arr})

    conn.commit()
    cursor.close()
    conn.close()


# Funkcja do przekształcenia obrazu w kwadratowy format
def make_square(image, size):
    width, height = image.size
    if width == height:
        return image

    max_dim = max(width, height)
    new_image = Image.new("RGB", (max_dim, max_dim), "black")
    offset = ((max_dim - width) // 2, (max_dim - height) // 2)
    new_image.paste(image, offset)
    return new_image.resize((size, size), Image.Resampling.LANCZOS)


# Lista ID obrazów do przetworzenia
image_ids = [1, 2, 3]  # <-- Zmień na rzeczywiste ID z tabeli `data`

for image_id in image_ids:
    image = get_image_from_db(image_id)
    if image:
        processed_image = make_square(image, max(image.size))
        save_processed_image(image_id, processed_image)
        print(f"Przetworzono obraz ID: {image_id}")
    else:
        print(f"Nie znaleziono obrazu o ID: {image_id}")

print("Przetwarzanie zakończone.")
