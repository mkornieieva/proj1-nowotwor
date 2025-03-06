from pathlib import Path
from app import main_panel
from main_panel import PhotoViewer
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, filedialog
from PIL import Image, ImageTk
from config import ASSETS_PATH, OUTPUT_PATH
import tkinter as tk
from config import relative_to_assets


window = Tk()
window.geometry("1321x700")
window.configure(bg="#000000")
viewer = PhotoViewer(window)

canvas = Canvas(
    window,
    bg="#000000",
    height=700,
    width=1321,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas.place(x=0, y=0)

image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
canvas.create_image(660, 350, image=image_image_1)

entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
entry_1 = Entry(
    bd=0,
    bg="#717171",
    fg="#FFFFFF",
    highlightthickness=0
)
entry_1.place(x=906, y=7, width=305, height=87)

canvas.create_text(18, 100, anchor="nw", text="Szukaj", fill="#FFFFFF", font=("Inter Bold", -18))

button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=200,
    highlightbackground="#555555",
    activebackground="#555555",
    command=viewer.zoom_in,
    relief="flat"
)
button_1.place(x=322, y=33, width=30, height=32)

entry_image_2 = PhotoImage(file=relative_to_assets("entry_2.png"))
canvas.create_image(143, 113, image=entry_image_2)
entry_2 = Entry(
    bd=0,
    bg="#6C6C6C",
    fg="#FFFFFF",
    highlightthickness=0
)
entry_2.place(x=82, y=103, width=123, height=18)

def show_menu():
    x = button_2.winfo_rootx()
    y = button_2.winfo_rooty() + button_2.winfo_height()
    menu.post(x, y)

button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))

button_2 = Button(
    window,
    image=button_image_2,
    borderwidth=0,
    highlightthickness=200,
    command=show_menu,
    relief="flat"
)
button_2.place(x=244, y=32, width=33, height=35)

menu = tk.Menu(window, tearoff=0)
menu.add_command(label="Importuj plik", command=lambda: print("opcja1"))
menu.add_command(label="Importuj folder", command=lambda: print("opcja2"))

button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=200,
    highlightbackground="#555555",
    activebackground="#555555",
    command=lambda: print("linie"),
    relief="flat"
)
button_3.place(x=456, y=32, width=33, height=35)

button_image_4 = PhotoImage(file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=200,
    highlightbackground="#555555",
    activebackground="#555555",
    command=viewer.save_image,
    relief="flat"
)
button_4.place(x=359, y=33, width=29, height=31)

button_image_5 = PhotoImage(file=relative_to_assets("button_5.png"))
button_5 = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=200,
    highlightbackground="#555555",
    activebackground="#555555",
    command=lambda: print("łapka"),
    relief="flat"
)
button_5.place(x=286, y=33, width=30, height=31)

button_image_6 = PhotoImage(file=relative_to_assets("button_6.png"))
button_6 = Button(
    image=button_image_6,
    borderwidth=0,
    highlightthickness=200,
    highlightbackground="#555555",
    activebackground="#555555",
    command=lambda: print("heatmap"),
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

    info_label = tk.Label(content_frame, text="informacje jszcze do uzupelnienia",
                          bg="#555555", fg="white", font=("Arial", 10))
    info_label.pack(expand=True)

    close_button = tk.Button(content_frame, text="Zamknij", command=popup.destroy)
    close_button.pack(pady=5)


button_image_7 = PhotoImage(file=relative_to_assets("button_7.png"))
button_7 = Button(
    image=button_image_7,
    borderwidth=0,
    highlightthickness=200,
    highlightbackground="#555555",
    activebackground="#555555",
    command= show_popup,
    relief="flat"
)
button_7.place(x=1240, y=42, width=22, height=23)


window.resizable(False, False)
window.mainloop()
