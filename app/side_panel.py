import os
import tkinter as tk
from tkinter import filedialog, Button
from PIL import Image, ImageTk
from config import relative_to_assets

grid_slots = [None, None, None, None]
displayed_images = {}

def choose_folder(folder, file, window):
    folder_path = filedialog.askdirectory(title="Wybierz folder")
    if folder_path:
        for widget in folder.winfo_children():
            widget.destroy()
        for widget in file.winfo_children():
            widget.destroy()
        try:
            entries = os.listdir(folder_path)
        except Exception as e:
            print(f"Błąd przy odczycie folderu: {e}")
            return

        def on_folder_click(path):
            list_files_in_folder(path, file, window)

        base_button = Button(folder, text=os.path.basename(folder_path) or folder_path,
                             bg="#555555", fg="white",
                             command=lambda: on_folder_click(folder_path))
        base_button.pack(fill="x", padx=5, pady=2)
        subfolders = [entry for entry in entries if os.path.isdir(os.path.join(folder_path, entry))]
        for sub in subfolders:
            sub_path = os.path.join(folder_path, sub)
            btn = Button(folder, text=sub, bg="#555555", fg="white",
                         command=lambda p=sub_path: on_folder_click(p))
            btn.pack(fill="x", padx=5, pady=2)

def list_files_in_folder(folder_path, file, window):
    for widget in file.winfo_children():
        widget.destroy()
    try:
        entries = os.listdir(folder_path)
    except Exception as e:
        print(f"Błąd przy odczycie folderu: {e}")
        return
    image_extensions = ('.png', '.jpg', '.jpeg', '.gif')
    image_files = [f for f in entries if f.lower().endswith(image_extensions) and
                   os.path.isfile(os.path.join(folder_path, f))]
    for file_name in image_files:
        full_path = os.path.join(folder_path, file_name)
        # Tworzymy ramkę podobną do add_image_to_side_panel
        frame = tk.Frame(file, bg="#555555")
        frame.pack(pady=2, fill="x")
        frame.file_name = file_name  # zapisujemy nazwę pliku dla wyszukiwania

        # Ładujemy miniaturkę
        try:
            img = Image.open(full_path)
            img.thumbnail((50, 50))
            thumbnail = ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Błąd przy tworzeniu miniaturki: {e}")
            continue

        label = tk.Label(frame, image=thumbnail, bg="#555555")
        label.image = thumbnail
        label.pack(side="left", padx=5)

        # Skracamy nazwę, jeśli jest długa
        max_length = 10
        display_name = file_name if len(file_name) <= max_length else file_name[:max_length] + "..."
        text = tk.Label(frame, text=display_name, fg="white", bg="#555555")
        text.pack(side="left")

        # Ładujemy ikonę "eye.png"
        eye_icon = Image.open(relative_to_assets("eye.png"))
        eye_icon = eye_icon.resize((20, 20), Image.Resampling.LANCZOS)
        eye_icon = ImageTk.PhotoImage(eye_icon)
        eye_btn = tk.Button(frame, image=eye_icon, bg="#555555", borderwidth=0)
        eye_btn.image = eye_icon  # zachowujemy referencję
        eye_btn.pack(side="right", padx=5)

        # Ustawiamy polecenie, które przełącza stan obrazu (podobnie jak w add_image_to_side_panel)
        eye_btn.config(command=lambda path=full_path, btn=eye_btn: toggle_image_display(path, window, btn))
        frame.bind("<Button-1>", lambda e, path=full_path, btn=eye_btn: toggle_image_display(path, window, btn))
        label.bind("<Button-1>", lambda e, path=full_path, btn=eye_btn: toggle_image_display(path, window, btn))
        text.bind("<Button-1>", lambda e, path=full_path, btn=eye_btn: toggle_image_display(path, window, btn))


def open_image_in_main_panel(filepath, window):
    for i in range(4):
        if grid_slots[i] is None:
            try:
                image = Image.open(filepath)
                image.thumbnail((300, 300))
                img = ImageTk.PhotoImage(image)
            except Exception as e:
                print(f"Błąd przy otwieraniu obrazu: {e}")
                return None
            row = i // 2
            col = i % 2
            frame = tk.Frame(window, bg="#000000")
            frame.place(x=320 + col * 520, y=110 + row * 300, width=300, height=300)
            label = tk.Label(frame, image=img, bg="#000000")
            label.image = img  # Zachowujemy referencję
            label.pack()
            frame.slot_index = i
            grid_slots[i] = frame
            return frame
    return None

def remove_image(frame):
    idx = frame.slot_index
    frame.destroy()
    grid_slots[idx] = None

def toggle_image_display(filepath, window, eye_btn=None):

    if filepath not in displayed_images:
        frame = open_image_in_main_panel(filepath, window)
        if frame is not None:
            displayed_images[filepath] = frame
            if eye_btn is not None:
                new_icon = Image.open(relative_to_assets("eye-crossed.png"))
                new_icon = new_icon.resize((20, 20), Image.Resampling.LANCZOS)
                new_icon = ImageTk.PhotoImage(new_icon)
                eye_btn.config(image=new_icon)
                eye_btn.image = new_icon
    else:
        frame = displayed_images[filepath]
        remove_image(frame)
        del displayed_images[filepath]
        if eye_btn is not None:
            new_icon = Image.open(relative_to_assets("eye.png"))
            new_icon = new_icon.resize((20, 20), Image.Resampling.LANCZOS)
            new_icon = ImageTk.PhotoImage(new_icon)
            eye_btn.config(image=new_icon)
            eye_btn.image = new_icon
