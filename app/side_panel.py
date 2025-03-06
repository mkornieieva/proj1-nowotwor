import os
import tkinter as tk
from tkinter import filedialog
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, filedialog
from PIL import Image, ImageTk


def choose_folder(folder, file):
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
            list_files_in_folder(path)
        base_button = Button(folder, text=os.path.basename(folder_path) or folder_path,
                             bg="#555555", fg="white", command=lambda: on_folder_click(folder_path))
        base_button.pack(fill="x", padx=5, pady=2)
        subfolders = [entry for entry in entries if os.path.isdir(os.path.join(folder_path, entry))]
        for sub in subfolders:
            sub_path = os.path.join(folder_path, sub)
            btn = Button(folder, text=sub, bg="#555555", fg="white",
                         command=lambda p=sub_path: on_folder_click(p))
            btn.pack(fill="x", padx=5, pady=2)

def list_files_in_folder(folder_path, file):
    for widget in file.winfo_children():
        widget.destroy()
    try:
        entries = os.listdir(folder_path)
    except Exception as e:
        print(f"Błąd przy odczycie folderu: {e}")
        return
    image_extensions = ('.png', '.jpg', '.jpeg', '.gif')
    image_files = [f for f in entries if f.lower().endswith(image_extensions) and os.path.isfile(os.path.join(folder_path, f))]
    for file_name in image_files:
        full_path = os.path.join(folder_path, file_name)
        file_frame = tk.Frame(file, bg="#666666", bd=1, relief="solid")
        file_frame.pack(fill="x", padx=5, pady=2)
        try:
            img = Image.open(full_path)
            img.thumbnail((50, 50))
            thumb = ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Błąd przy ładowaniu miniaturki: {e}")
            thumb = None
        if thumb:
            thumb_label = tk.Label(file_frame, image=thumb, bg="#666666")
            thumb_label.image = thumb
            thumb_label.pack(side="left", padx=5)
        else:
            thumb_label = tk.Label(file_frame, text="Brak", bg="#666666", fg="white")
            thumb_label.pack(side="left", padx=5)
        name_label = tk.Label(file_frame, text=file_name, bg="#666666", fg="white")
        name_label.pack(side="left", padx=5)
        display_btn = Button(file_frame, text="Wyświetl", bg="#555555", fg="white",
                             command=lambda: "co")
        display_btn.pack(side="left", padx=5)
        remove_btn = Button(file_frame, text="Usuń", bg="#555555", fg="white",
                            command=lambda f=file_frame: f.destroy())
        remove_btn.pack(side="left", padx=5)

