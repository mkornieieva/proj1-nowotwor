import cx_Oracle
from PIL import Image
import io

# Dane do połączenia z bazą
DB_USER = "nowotwor_user"
DB_PASSWORD = "nowotwor_eiti"
DB_DSN = "localhost/XEPDB1"

TARGET_SIZE = (256, 256)  # Docelowy rozmiar obrazów


def get_db_connection():
    return cx_Oracle.connect(DB_USER, DB_PASSWORD, DB_DSN)


def fetch_images_from_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT proc_image_id, image_data FROM ProcessedImages")

    images = []
    for image_id, image_blob in cursor:
        images.append((image_id, image_blob.read()))

    cursor.close()
    conn.close()
    return images

#Przetwarza obraz (zmiana rozmiaru na 256x256)
def process_image(image_data):
    image = Image.open(io.BytesIO(image_data))
    resized_image = image.resize(TARGET_SIZE, Image.Resampling.LANCZOS)

    output = io.BytesIO()
    resized_image.save(output, format="PNG")  # Zapisujemy w formacie PNG
    return output.getvalue()


#Zapisuje przetworzony obraz do bazy
def save_image_to_db(image_id, processed_image_data):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE ProcessedImages
        SET image_data = :image_data
        WHERE proc_image_id = :image_id
    """, {"image_id": image_id, "image_data": processed_image_data})

    conn.commit()
    cursor.close()
    conn.close()

#Główna funkcja przetwarzania obrazów
def main():

    images = fetch_images_from_db()

    for image_id, image_data in images:
        try:
            processed_image_data = process_image(image_data)
            save_image_to_db(image_id, processed_image_data)
            print(f"Przetworzono obraz o ID: {image_id}")
        except Exception as e:
            print(f"Błąd podczas przetwarzania obrazu ID {image_id}: {e}")

    print("Koniec przetwarzania!")


if __name__ == "__main__":
    main()
