from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, filedialog
from PIL import Image, ImageTk

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"../app/assets/frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class PhotoViewer:
    def __init__(self, master):
        self.master = master
        self.zoom_level = 100
        self.current_index = -1
        self.image_list = []

        self.image_frame = Canvas(
            master,
            bg="#555555",
            height=150,
            width=350,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.image_frame.place(x=600, y=350)

    def open_image(self):
        file_path = filedialog.askopenfilename(
            title="Select Image", filetypes=(("PNG", "*.png"), ("JPEG", "*.jpg"))
        )
        if file_path:
            try:
                image = Image.open(file_path)
                self.image_list.append(image)
                self.current_index = len(self.image_list) - 1
                print(f"Loaded image: {file_path}, size: {image.size}")  # Debugowanie
                self.display_image()
            except Exception as e:
                print(f"Error loading image: {e}")

    def save_image(self):
        if self.current_index != -1:
            file_path = filedialog.asksaveasfilename(
                title="Save Image",
                filetypes=[("JPEG Image", "*.jpg"), ("PNG Image", "*.png")],
                defaultextension=".png",
            )
            if file_path:
                self.image_list[self.current_index].save(file_path)

    def zoom_in(self):
        if self.current_index != -1:
            image = self.image_list[self.current_index]
            width, height = image.size
            new_width = int(width * 1.1)
            new_height = int(height * 1.1)
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS
)
            self.image_list[self.current_index] = image
            self.display_image()

    def zoom_out(self):
        if self.current_index != -1:
            image = self.image_list[self.current_index]
            width, height = image.size
            new_width = int(width / 1.1)
            new_height = int(height / 1.1)
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS
)
            self.image_list[self.current_index] = image
            self.display_image()

    def display_image(self):
        if self.current_index != -1:
            image = self.image_list[self.current_index]
            width, height = image.size

            # Resize the image to 1/4 of its original size
            new_width = width // 4
            new_height = height // 4
            resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS

)

            # Create a PhotoImage from the resized image
            photo = ImageTk.PhotoImage(resized_image)

            # Clear the canvas and display the resized image
            self.image_frame.delete("all")
            self.image_frame.config(scrollregion=(0, 0, new_width, new_height))
            self.image_frame.create_image(0, 0, image=photo, anchor="nw")

            # Store a reference to the photo to prevent garbage collection
            self.image_frame.image = photo

window = Tk()

window.geometry("1321x700")
window.configure(bg="#555555")
viewer = PhotoViewer(window)

canvas = Canvas(
    window,
    bg="#555555",
    height=700,
    width=1321,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

canvas.place(x=0, y=0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    660.0,
    350.0,
    image=image_image_1
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    1059.2923889160156,
    51.51327133178711,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#717171",
    fg="#FFFFFF",
    highlightthickness=0
)
entry_1.place(
    x=906.778564453125,
    y=7.0,
    width=305.02764892578125,
    height=87.02654266357422
)

canvas.create_text(
    18.0,
    100.0,
    anchor="nw",
    text="Szukaj",
    fill="#FFFFFF",
    font=("Inter Bold", 18 * -1)
)

# Update buttons with correct properties
button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=200,  # Set highlight thickness to 200
    highlightbackground="#555555",  # Correct property for highlight background
    activebackground="#555555",  # Ensure the color remains consistent on hover
    command=viewer.zoom_in,
    relief="flat"
)
button_1.place(
    x=322.0149230957031,
    y=33.01190185546875,
    width=30.484512329101562,
    height=32.30758285522461
)

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    143.5,
    113.0,
    image=entry_image_2
)
entry_2 = Entry(
    bd=0,
    bg="#6C6C6C",
    fg="#FFFFFF",
    highlightthickness=0
)
entry_2.place(
    x=82.0,
    y=103.0,
    width=123.0,
    height=18.0
)

# Repeat for other buttons
button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=200,
    highlightbackground="#555555",  # Correct property
    activebackground="#555555",
    command=viewer.open_image,
    relief="flat"
)
button_2.place(
    x=244.87094116210938,
    y=32.9481201171875,
    width=33.086151123046875,
    height=35.052635192871094
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=200,
    highlightbackground="#555555",
    activebackground="#555555",
    command=lambda: print("linie"),
    relief="flat"
)
button_3.place(
    x=456.0598449707031,
    y=32.390228271484375,
    width=33.086151123046875,
    height=35.052635192871094
)

button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=200,
    highlightbackground="#555555",
    activebackground="#555555",
    command=viewer.save_image,
    relief="flat"
)
button_4.place(
    x=359.0745849609375,
    y=33.6453857421875,
    width=29.289043426513672,
    height=31.040620803833008
)

button_image_5 = PhotoImage(
    file=relative_to_assets("button_5.png"))
button_5 = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=200,
    highlightbackground="#555555",
    activebackground="#555555",
    command=lambda: print("łapka"),
    relief="flat"
)
button_5.place(
    x=286.1911315917969,
    y=33.467437744140625,
    width=30.222583770751953,
    height=31.602924346923828
)

button_image_6 = PhotoImage(
    file=relative_to_assets("button_6.png"))
button_6 = Button(
    image=button_image_6,
    borderwidth=0,
    highlightthickness=200,
    highlightbackground="#555555",
    activebackground="#555555",
    command=lambda: print("heatmap"),
    relief="flat"
)
button_6.place(
    x=413.9458312988281,
    y=32.25079345703125,
    width=34.90947723388672,
    height=36.62346649169922
)

button_image_7 = PhotoImage(
    file=relative_to_assets("button_7.png"))
button_7 = Button(
    image=button_image_7,
    borderwidth=0,
    highlightthickness=200,
    highlightbackground="#555555",
    activebackground="#555555",
    command=lambda: print("info"),
    relief="flat"
)
button_7.place(
    x=1240.4642333984375,
    y=42.0,
    width=22.323211669921875,
    height=23.649993896484375
)

window.resizable(False, False)
window.mainloop()