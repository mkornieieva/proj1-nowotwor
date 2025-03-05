from tkinter import Canvas, filedialog
from PIL import Image, ImageTk
import tkinter as tk

class PhotoViewer:
    def __init__(self, master, window_width=1321, window_height=700):
        self.master = master
        self.current_index = -1  # indeks aktualnie aktywnego obrazu
        self.image_list = []  # lista załadowanych obrazów

        # Obliczamy obszar, który ma zajmować PhotoViewer (5/6 okna, wyrównany do prawego dolnego rogu)
        grid_width = int(window_width * 5 / 6)
        grid_height = int(window_height * 5 / 6)
        grid_x0 = window_width - grid_width  # czyli window_width/6
        grid_y0 = window_height - grid_height  # czyli window_height/6

        # Podział na 4 ćwiartki (układ 2x2)
        quad_w = grid_width // 2
        quad_h = grid_height // 2
        self.quadrants = [
            {"x": grid_x0, "y": grid_y0, "w": quad_w, "h": quad_h},  # górny lewy
            {"x": grid_x0 + quad_w, "y": grid_y0, "w": quad_w, "h": quad_h},  # górny prawy
            {"x": grid_x0, "y": grid_y0 + quad_h, "w": quad_w, "h": quad_h},  # dolny lewy
            {"x": grid_x0 + quad_w, "y": grid_y0 + quad_h, "w": quad_w, "h": quad_h}  # dolny prawy
        ]

        # Utwórz canvasy dla każdej ćwiartki
        self.image_frames = []
        for quad in self.quadrants:
            frame = Canvas(
                master,
                bg="#000000",
                width=quad["w"],
                height=quad["h"],
                bd=0,
                highlightthickness=0,
                relief="ridge"
            )
            frame.place(x=quad["x"], y=quad["y"])
            self.image_frames.append(frame)

    def open_image(self):
        if len(self.image_list) >= 4:
            print("Już załadowano 4 obrazy.")
            return
        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=(("PNG", "*.png"), ("JPEG", "*.jpg"))
        )
        if file_path:
            try:
                image = Image.open(file_path)
                self.image_list.append(image)
                self.current_index = len(self.image_list) - 1
                print(f"Załadowano obraz: {file_path}, rozmiar: {image.size}")
                self.display_image(self.current_index)
            except Exception as e:
                print(f"Błąd przy ładowaniu obrazu: {e}")

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
            quad = self.quadrants[self.current_index]
            max_w, max_h = quad["w"], quad["h"]
            scale = 1.1
            # Ograniczenie, aby obraz nie przekroczył obszaru canvasa
            if width * scale > max_w or height * scale > max_h:
                scale = min(max_w / width, max_h / height)
            new_width = int(width * scale)
            new_height = int(height * scale)
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            self.image_list[self.current_index] = image
            self.display_image(self.current_index)

    def zoom_out(self):
        if self.current_index != -1:
            image = self.image_list[self.current_index]
            width, height = image.size
            new_width = int(width / 1.1)
            new_height = int(height / 1.1)
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            self.image_list[self.current_index] = image
            self.display_image(self.current_index)

    def display_image(self, index):
        if index < len(self.image_list):
            image = self.image_list[index]
            quad = self.quadrants[index]
            max_w, max_h = quad["w"], quad["h"]
            width, height = image.size
            if width > max_w or height > max_h:
                ratio = min(max_w / width, max_h / height)
                new_width = int(width * ratio)
                new_height = int(height * ratio)
                display_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            else:
                display_image = image
            photo = ImageTk.PhotoImage(display_image)
            canvas_img = self.image_frames[index]
            canvas_img.delete("all")
            canvas_img.create_image(max_w // 2, max_h // 2, image=photo, anchor="center")
            canvas_img.image = photo

    def display_all_images(self):
        for i in range(len(self.image_list)):
            self.display_image(i)
