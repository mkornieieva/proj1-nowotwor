import os
import cv2
import tkinter as tk
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, filedialog
from PIL import Image, ImageTk
from config import relative_to_assets
import side_panel
from main_panel import zoom_image, drag, select_main_frame
from previous_configurations.app.export_to_pdf import export_main_panel_to_pdf

window = Tk()
window.geometry("1321x700")
window.configure(bg="#000000")


canvas = Canvas(window, bg="#000000", height=700, width=1321, bd=0, highlightthickness=0, relief="ridge")
canvas.place(x=0, y=0)


image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
canvas.create_image(660, 350, image=image_image_1)

entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
entry_1 = Entry(window, bd=0, bg="#717171", fg="#FFFFFF", highlightthickness=0)
entry_1.place(x=906, y=7, width=305, height=87)

canvas.create_text(18, 100, anchor="nw", text="Szukaj", fill="#FFFFFF", font=("Inter Bold", -18))


button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
button_1 = Button(window, image=button_image_1, borderwidth=0, highlightthickness=200,
                  highlightbackground="#555555", activebackground="#555555", bg="#555555",
                  command=zoom_image, relief="flat")
button_1.place(x=322, y=33, width=30, height=32)

entry_image_2 = PhotoImage(file=relative_to_assets("entry_2.png"))
canvas.create_image(143, 113, image=entry_image_2)
entry_2 = Entry(window, bd=0, bg="#6C6C6C", fg="#FFFFFF", highlightthickness=0)
entry_2.place(x=82, y=103, width=123, height=18)

def search_files(event=None):
    query = entry_2.get().lower()
    for widget in side_panel.all_image_frames:
        if query in widget.file_name.lower():
            widget.pack(pady=2, fill="x")
        else:
            widget.pack_forget()

entry_2.bind("<KeyRelease>", search_files)


def show_menu():
    x = button_2.winfo_rootx()
    y = button_2.winfo_rooty() + button_2.winfo_height()
    menu.post(x, y)

button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
button_2 = Button(window, image=button_image_2, borderwidth=0, highlightthickness=200,
                  highlightbackground="#555555", activebackground="#555555", bg="#555555",
                  command=show_menu, relief="flat")
button_2.place(x=244, y=32, width=33, height=35)

menu = tk.Menu(window, tearoff=0)
menu.add_command(label="Importuj plik", command=lambda: import_file())
menu.add_command(label="Importuj folder", command=lambda: side_panel.choose_folder(folder_list_frame, file_list_frame, window, side_panel.all_image_frames))

button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
button_3 = Button(window, image=button_image_3, borderwidth=0, highlightthickness=200,
                  highlightbackground="#555555", activebackground="#555555", bg="#555555",
                  command=lambda: print("linie"), relief="flat")
button_3.place(x=456, y=32, width=33, height=35)

button_image_4 = PhotoImage(file=relative_to_assets("button_4.png"))
button_4 = Button(window, image=button_image_4, borderwidth=0, highlightthickness=200,
                  highlightbackground="#555555", activebackground="#555555", bg="#555555",
                  command=lambda: export_main_panel_to_pdf(window), relief="flat")
button_4.place(x=359, y=33, width=29, height=31)

button_image_5 = PhotoImage(file=relative_to_assets("button_5.png"))
button_5 = Button(window, image=button_image_5, borderwidth=0, highlightthickness=200,
                  highlightbackground="#555555", activebackground="#555555", bg="#555555",
                  command=drag, relief="flat")
button_5.place(x=286, y=33, width=30, height=31)

button_image_6 = PhotoImage(file=relative_to_assets("button_6.png"))
button_6 = Button(
    window,
    image=button_image_6,
    command=lambda: run_model_on_selected_image(),
    borderwidth=0, highlightthickness=200,
    highlightbackground="#555555",
    activebackground="#555555", bg="#555555",
    relief="flat"
)
button_6.place(x=413, y=32, width=34, height=36)


def show_popup():
    popup = tk.Toplevel(window)
    popup.geometry("300x90+950+80")
    popup.resizable(False, False)
    popup.overrideredirect(False)
    border_frame = tk.Frame(popup, bg="white", padx=2, pady=2)
    border_frame.pack(expand=True, fill="both")
    content_frame = tk.Frame(border_frame, bg="#555555")
    content_frame.pack(expand=True, fill="both")
    info_label = tk.Label(content_frame, text="informacje jeszcze do uzupełnienia", bg="#555555", fg="white", font=("Arial", 10))
    info_label.pack(expand=True)
    close_button = tk.Button(content_frame, text="Zamknij", command=popup.destroy)
    close_button.pack(pady=5)


def show_prediction_popup(result):
    popup = tk.Toplevel(window)
    popup.geometry("300x100+950+80")
    popup.resizable(False, False)
    popup.overrideredirect(False)

    border_frame = tk.Frame(popup, bg="white", padx=2, pady=2)
    border_frame.pack(expand=True, fill="both")

    content_frame = tk.Frame(border_frame, bg="#555555")
    content_frame.pack(expand=True, fill="both")

    info_label = tk.Label(content_frame, text=result, bg="#555555", fg="white", font=("Arial", 12))
    info_label.pack(expand=True)

    close_button = tk.Button(content_frame, text="Zamknij", command=popup.destroy)
    close_button.pack(pady=5)


button_image_7 = PhotoImage(file=relative_to_assets("button_7.png"))
button_7 = Button(window, image=button_image_7, borderwidth=0, highlightthickness=200,
                  highlightbackground="#555555", activebackground="#555555", bg="#555555",
                  command=show_popup, relief="flat")
button_7.place(x=1240, y=42, width=22, height=23)


file_explorer_frame = tk.Frame(window, bg="#333333")
file_explorer_frame.place(x=10, y=130, width=195, height=560)
nametag = tk.Label(file_explorer_frame, text="Lista skanów", bg="#555555", fg="white")
nametag.pack(pady=5, fill="x")

folder_label = tk.Label(file_explorer_frame, text="Foldery:", bg="#333333", fg="white")
folder_label.pack(pady=(10, 0))
folder_list_frame = tk.Frame(file_explorer_frame, bg="#444444")
folder_list_frame.pack(pady=5, fill="x")

file_label = tk.Label(file_explorer_frame, text="Pliki:", bg="#333333", fg="white")
file_label.pack(pady=(10, 0))

file_list_canvas = tk.Canvas(file_explorer_frame, bg="#444444", borderwidth=0, highlightthickness=0)
file_list_canvas.pack(side=tk.LEFT, fill="both", expand=True)

scrollbar = tk.Scrollbar(file_explorer_frame, orient=tk.VERTICAL, command=file_list_canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill="y")
file_list_canvas.configure(yscrollcommand=scrollbar.set)

file_list_frame = tk.Frame(file_list_canvas, bg="#444444")
canvas_window = file_list_canvas.create_window((0, 0), window=file_list_frame, anchor="nw")

def on_frame_configure(event):
    file_list_canvas.configure(scrollregion=file_list_canvas.bbox("all"))
file_list_frame.bind("<Configure>", on_frame_configure)

def on_canvas_configure(event):
    file_list_canvas.itemconfig(canvas_window, width=event.width)
file_list_canvas.bind("<Configure>", on_canvas_configure)

def _on_mousewheel(event):
    file_list_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
file_list_canvas.bind("<Enter>", lambda e: file_list_canvas.bind_all("<MouseWheel>", _on_mousewheel))
file_list_canvas.bind("<Leave>", lambda e: file_list_canvas.unbind_all("<MouseWheel>"))

def add_image_to_side_panel(filepath):
    filename = os.path.basename(filepath)
    max_length = 10
    display_name = filename if len(filename) <= max_length else filename[:max_length] + "..."

    img_pil = Image.open(filepath)
    img_pil.thumbnail((50, 50))
    thumbnail = ImageTk.PhotoImage(img_pil)

    frame = tk.Frame(file_list_frame, bg="#555555")
    frame.pack(pady=2, fill="x")
    frame.file_name = filename
    side_panel.all_image_frames.append(frame)

    label = tk.Label(frame, image=thumbnail, bg="#555555")
    label.image = thumbnail
    label.pack(side="left", padx=5)

    text = tk.Label(frame, text=display_name, fg="white", bg="#555555")
    text.pack(side="left")

    eye_icon = Image.open(relative_to_assets("eye.png"))
    eye_icon = eye_icon.resize((20, 20), Image.Resampling.LANCZOS)
    eye_icon = ImageTk.PhotoImage(eye_icon)
    eye_btn = tk.Button(frame, image=eye_icon, bg="#555555", borderwidth=0,
                        command=lambda: side_panel.toggle_image_display(filepath, window, eye_btn))
    eye_btn.image = eye_icon
    eye_btn.pack(side="right", padx=5)

    frame.bind("<Button-1>", lambda e, path=filepath, btn=eye_btn, frm=frame: (
    side_panel.toggle_image_display(path, window, btn), select_main_frame(frm)))
    label.bind("<Button-1>", lambda e, path=filepath, btn=eye_btn, frm=frame: (
    side_panel.toggle_image_display(path, window, btn), select_main_frame(frm)))
    text.bind("<Button-1>", lambda e, path=filepath, btn=eye_btn, frm=frame: (
    side_panel.toggle_image_display(path, window, btn), select_main_frame(frm)))

def import_file():
    filepath = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.png;*.jpeg")])
    if filepath:
        add_image_to_side_panel(filepath)

def run_model_on_selected_image():
    from main_panel import selected_frame, update_main_image
    from model_loading.model_loading import predict_and_draw
    from __main__ import add_image_to_side_panel
    from side_panel import  all_image_frames


    if selected_frame is None or not hasattr(selected_frame, 'filepath'):
        print("Brak zaznaczonego obrazu w panelu głównym.")
        return

    original_path = selected_frame.filepath
    dir_name, file_name = os.path.split(original_path)
    name, ext = os.path.splitext(file_name)
    annotated_path = os.path.join(dir_name, f"{name}_ozn{ext}")

    if not os.path.exists(annotated_path):
        print("Generowanie oznaczonego obrazu...")
        result = predict_and_draw(original_path)
        cv2.imwrite(annotated_path, result)
        add_image_to_side_panel(annotated_path)
    else:
        print("Usuwanie oznaczonego obrazu i przywracanie oryginału...")
        try:
            os.remove(annotated_path)
        except Exception as e:
            print(f"Błąd usuwania pliku: {e}")

        # Usuwanie miniaturki z panelu bocznego
        for frame in all_image_frames[:]:
            if hasattr(frame, "file_name") and frame.file_name == f"{name}_ozn{ext}":
                frame.destroy()
                all_image_frames.remove(frame)
                print(f"Usunięto miniaturkę: {name}_ozn{ext}")
                break

        annotated_path = original_path  # wracamy do oryginału

    # Załaduj obraz (oryginalny lub oznaczony) i przekaż do update_main_image
    img = Image.open(annotated_path)
    img_tk = ImageTk.PhotoImage(img)
    update_main_image(img_tk)

window.resizable(False, False)
window.mainloop()
