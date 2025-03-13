from PIL import Image, ImageDraw, ImageFont
import os
import tkinter as tk


def get_pdf_filename(master):
    filename = None

    def on_ok():
        nonlocal filename
        filename = entry.get().strip()
        if filename and not filename.lower().endswith(".pdf"):
            filename += ".pdf"
        dialog.destroy()

    dialog = tk.Toplevel(master)
    dialog.title("Podaj nazwę pliku PDF")
    dialog.grab_set()  # blokuje interakcję z głównym oknem

    tk.Label(dialog, text="Nazwa pliku:").pack(padx=10, pady=10)
    entry = tk.Entry(dialog, width=40)
    entry.pack(padx=10, pady=5)
    entry.focus_set()

    ok_button = tk.Button(dialog, text="OK", command=on_ok)
    ok_button.pack(pady=10)

    dialog.wait_window()
    return filename


def export_main_panel_to_pdf(master, output_path=None, description_height=100, margin=20):
    if output_path is None:
        output_path = get_pdf_filename(master)
        if not output_path:
            print("Nie podano nazwy pliku. Anulowano eksport PDF.")
            return


    try:
        from side_panel import grid_slots
    except ImportError as e:
        print("Błąd importu grid_slots z side_panel:", e)
        return


    images_list = []
    for frame in grid_slots:
        if frame is not None and hasattr(frame, 'filepath'):
            print("Przetwarzanie obrazu:", frame.filepath)
            try:
                img = Image.open(frame.filepath).convert("RGB")
                images_list.append(img)
            except Exception as e:
                print("Błąd przy otwieraniu obrazu:", frame.filepath, e)

    if not images_list:
        print("Brak obrazów do eksportu.")
        return


    max_width = max(img.width for img in images_list)
    images_with_description = []
    total_height = 0

    for img in images_list:
        # Jeśli obraz jest węższy niż max_width, wyśrodkowujemy go na tle o szerokości max_width
        if img.width < max_width:
            padded = Image.new("RGB", (max_width, img.height), "black")
            padded.paste(img, ((max_width - img.width) // 2, 0))
            img = padded

        new_height = img.height + description_height
        combined = Image.new("RGB", (max_width, new_height), "black")
        combined.paste(img, (0, 0))
        draw = ImageDraw.Draw(combined)
        text = "Opis: "
        text_x = 10
        text_y = img.height + (description_height - 20) // 2  # centrowanie tekstu w obszarze opisu
        draw.text((text_x, text_y), text, fill="white")
        images_with_description.append(combined)
        total_height += combined.height + margin

    total_height -= margin

    combined_image = Image.new("RGB", (max_width, total_height), "black")
    y_offset = 0
    for im in images_with_description:
        combined_image.paste(im, (0, y_offset))
        y_offset += im.height + margin

    try:
        combined_image.save(output_path, "PDF", resolution=100.0)
        print("Obrazy zapisane do pliku:", output_path)
    except Exception as e:
        print("Błąd zapisu PDF:", e)
