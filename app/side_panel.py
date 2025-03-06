import tkinter as tk

file_explorer_frame = tk.Frame(window, bg="#333333")
file_explorer_frame.place(x=10, y=130, width=200, height=560)
folder_select_button = Button(file_explorer_frame, text="Wybierz folder", bg="#555555", fg="white",
                              command=lambda: choose_folder())
folder_select_button.pack(pady=5, fill="x")

folder_label = tk.Label(file_explorer_frame, text="Foldery:", bg="#333333", fg="white")
folder_label.pack(pady=(10, 0))
folder_list_frame = tk.Frame(file_explorer_frame, bg="#444444")
folder_list_frame.pack(pady=5, fill="x")

file_label = tk.Label(file_explorer_frame, text="Pliki:", bg="#333333", fg="white")
file_label.pack(pady=(10, 0))
file_list_frame = tk.Frame(file_explorer_frame, bg="#444444")
file_list_frame.pack(pady=5, fill="both", expand=True)

def choose_folder():
    folder_path = filedialog.askdirectory(title="Wybierz folder")
    if folder_path:
        for widget in folder_list_frame.winfo_children():
            widget.destroy()
        for widget in file_list_frame.winfo_children():
            widget.destroy()
        try:
            entries = os.listdir(folder_path)
        except Exception as e:
            print(f"Błąd przy odczycie folderu: {e}")
            return
        def on_folder_click(path):
            list_files_in_folder(path)
        base_button = Button(folder_list_frame, text=os.path.basename(folder_path) or folder_path,
                             bg="#555555", fg="white", command=lambda: on_folder_click(folder_path))
        base_button.pack(fill="x", padx=5, pady=2)
        subfolders = [entry for entry in entries if os.path.isdir(os.path.join(folder_path, entry))]
        for sub in subfolders:
            sub_path = os.path.join(folder_path, sub)
            btn = Button(folder_list_frame, text=sub, bg="#555555", fg="white",
                         command=lambda p=sub_path: on_folder_click(p))
            btn.pack(fill="x", padx=5, pady=2)

def list_files_in_folder(folder_path):
    for widget in file_list_frame.winfo_children():
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
        file_frame = tk.Frame(file_list_frame, bg="#666666", bd=1, relief="solid")
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
                             command=lambda p=full_path: display_file_in_main_area(p))
        display_btn.pack(side="left", padx=5)
        remove_btn = Button(file_frame, text="Usuń", bg="#555555", fg="white",
                            command=lambda f=file_frame: f.destroy())
        remove_btn.pack(side="left", padx=5)

main_display_canvas = Canvas(window, bg="#000000", bd=2, relief="solid")
main_display_canvas.place(x=250, y=130, width=800, height=500)

def display_file_in_main_area(file_path):
    try:
        img = Image.open(file_path)
    except Exception as e:
        print(f"Błąd przy otwieraniu obrazu: {e}")
        return
    canvas_width = main_display_canvas.winfo_width()
    canvas_height = main_display_canvas.winfo_height()
    img_width, img_height = img.size
    ratio = min(canvas_width / img_width, canvas_height / img_height)
    new_width = int(img_width * ratio)
    new_height = int(img_height * ratio)
    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(img)
    main_display_canvas.delete("all")
    main_display_canvas.create_image(canvas_width//2, canvas_height//2, image=photo, anchor="center")
    main_display_canvas.image = photo.