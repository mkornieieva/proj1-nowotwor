import os
import zipfile
from PIL import Image

#ścieżki do zmiany
zip_path = r"C:\Users\klaud\Downloads\archive.zip"
extract_path = r"C:\Users\klaud\Downloads\extracted_data"
fixed_path = r"C:\Users\klaud\Downloads\extracted_data_fixed"



with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(extract_path)



if not os.path.exists(fixed_path):
    os.makedirs(fixed_path)



def make_square(image, size):

    width, height = image.size
    if width == height:
        return image


    max_dim = max(width, height)
    new_image = Image.new("RGB", (max_dim, max_dim), "black")
    offset = ((max_dim - width) // 2, (max_dim - height) // 2)


    new_image.paste(image, offset)
    return new_image.resize((size, size), Image.Resampling.LANCZOS)



for root, dirs, files in os.walk(extract_path):
    for file in files:
        if file.lower().endswith((".png", ".jpg", ".jpeg")):
            image_path = os.path.join(root, file)

            try:
                with Image.open(image_path) as img:
                    width, height = img.size

                    relative_path = os.path.relpath(root, extract_path)
                    save_dir = os.path.join(fixed_path, relative_path)

                    if not os.path.exists(save_dir):
                        os.makedirs(save_dir)


                    square_img = make_square(img, max(width, height))


                    save_path = os.path.join(save_dir, file)
                    square_img.save(save_path)

            except Exception as e:
                print(f"Błąd podczas przetwarzania zdjęcia {image_path}: {e}")

print(f"Przetwarzanie zakończone. Przetworzone zdjęcia zostały zapisane w folderze: {fixed_path}")