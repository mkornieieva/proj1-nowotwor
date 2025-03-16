import tkinter as tk
from tkinter import Canvas
from PIL import Image, ImageTk

selected_frame = None

def select_main_frame(frame):
    global selected_frame
    if selected_frame is not None and selected_frame.winfo_exists():
        selected_frame.config(highlightthickness=0)
    selected_frame = frame
    if frame.winfo_exists():
        frame.config(highlightthickness=2, highlightbackground="white")



def prepare_frame_for_zoom(frame):
    if not hasattr(frame, 'filepath'):
        print("Błąd: brak atrybutu 'filepath' w ramce.")
        return

    for child in frame.winfo_children():
        child.destroy()

    frame_width = 300
    frame_height = 300

    try:
        img = Image.open(frame.filepath)
    except Exception as e:
        print(f"Błąd otwierania obrazu: {e}")
        return

    img_ratio = img.width / img.height
    frame_ratio = frame_width / frame_height
    if img_ratio > frame_ratio:
        new_width = frame_width
        new_height = int(frame_width / img_ratio)
    else:
        new_height = frame_height
        new_width = int(frame_height * img_ratio)

    base_image = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    frame.base_image = base_image
    frame.current_scale = 1.0
    frame.image_offset_x = 0
    frame.image_offset_y = 0

    canvas = tk.Canvas(frame, width=frame_width, height=frame_height, bg=frame['bg'], highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    frame.canvas = canvas

    display_image = ImageTk.PhotoImage(base_image)
    frame.display_image = display_image
    frame.canvas_image = canvas.create_image(0, 0, anchor="nw", image=display_image)

def zoom_image():
    global selected_frame
    if selected_frame is None:
        print("Brak zaznaczonego obrazu. Wybierz obraz klikając na miniaturkę.")
        return

    if not hasattr(selected_frame, 'canvas'):
        prepare_frame_for_zoom(selected_frame)
        if not hasattr(selected_frame, 'canvas'):
            return

    if not hasattr(selected_frame, 'zoom_direction'):
        selected_frame.zoom_direction = "in"

    current_scale = selected_frame.current_scale

    if selected_frame.zoom_direction == "in":
        new_scale = current_scale + 0.25
        if new_scale >= 2.0:
            new_scale = 2.0
            selected_frame.zoom_direction = "out"
    else:
        new_scale = current_scale - 0.25
        if new_scale <= 1.0:
            new_scale = 1.0
            selected_frame.zoom_direction = "in"

    selected_frame.current_scale = new_scale


    base_img = selected_frame.base_image
    new_width = int(base_img.width * new_scale)
    new_height = int(base_img.height * new_scale)
    resized_img = base_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    new_photo = ImageTk.PhotoImage(resized_img)
    selected_frame.display_image = new_photo


    selected_frame.canvas.itemconfig(selected_frame.canvas_image, image=new_photo)
    selected_frame.canvas.config(scrollregion=(0, 0, new_width, new_height))


def drag():
    global selected_frame
    if selected_frame is None:
        print("Brak zaznaczonego obrazu.")
        return
    if not hasattr(selected_frame, 'canvas'):
        print("Obraz nie został przygotowany do przesuwania (brak Canvas).")
        return
    if selected_frame.current_scale <= 1.0:
        print("Obraz nie jest przybliżony – przesuwanie dostępne tylko przy powiększonym obrazie.")
        return

    selected_frame.canvas.bind("<ButtonPress-1>", on_drag_start)
    selected_frame.canvas.bind("<B1-Motion>", on_drag_motion)
    selected_frame.canvas.bind("<ButtonRelease-1>", on_drag_release)
    print("Włączono tryb przesuwania obrazu ('drag').")

def on_drag_start(event):
    canvas = event.widget
    canvas.drag_start_x = event.x
    canvas.drag_start_y = event.y

def on_drag_motion(event):
    canvas = event.widget
    dx = event.x - canvas.drag_start_x
    dy = event.y - canvas.drag_start_y
    canvas.move(selected_frame.canvas_image, dx, dy)
    canvas.drag_start_x = event.x
    canvas.drag_start_y = event.y

def on_drag_release(event):
    pass

def open_image_in_main_panel(filepath, window):
    from side_panel import grid_slots
    from PIL import Image, ImageTk
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
            label.image = img  # zachowanie referencji
            label.pack()
            frame.slot_index = i
            frame.filepath = filepath
            frame.bind("<Button-1>", lambda e, frm=frame: select_main_frame(frm))
            label.bind("<Button-1>", lambda e, frm=frame: select_main_frame(frm))
            grid_slots[i] = frame
            return frame
    return None

def remove_image(frame):
    from side_panel import grid_slots
    idx = frame.slot_index
    frame.destroy()
    grid_slots[idx] = None
