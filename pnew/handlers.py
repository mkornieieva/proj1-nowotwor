import os
from PySide6.QtWidgets import QFileDialog, QLabel, QVBoxLayout, QWidget, QListWidgetItem
from PySide6.QtGui import QPixmap, QPainter, QPen, QColor, QFontMetrics
from PySide6.QtCore import Qt, QPoint

# Dozwolone rozszerzenia graficzne
ALLOWED_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.webp')


RESIZE_MARGIN = 8

def get_resize_direction(widget, pos):
    rect = widget.rect()
    x, y, w, h = rect.x(), rect.y(), rect.width(), rect.height()
    margin = RESIZE_MARGIN
    directions = []
    if pos.x() <= x + margin:
        directions.append("left")
    elif pos.x() >= x + w - margin:
        directions.append("right")
    if pos.y() <= y + margin:
        directions.append("top")
    elif pos.y() >= y + h - margin:
        directions.append("bottom")
    return "_".join(directions) if directions else None

# pobierz sciezki do obrazow
def get_image_paths(mode="folder", folder_path=None, parent=None):
    """
    Zwraca listę ścieżek do obrazów w zależności od trybu:
    - mode="folder": wczytuje wszystkie grafiki z folderu_path
    - mode="dialog": otwiera okno dialogowe do wyboru plików
    """
    image_files = []

    if mode == "folder":
        if not folder_path or not os.path.isdir(folder_path):
            print("Nieprawidłowa ścieżka do folderu.")
            return []
        for filename in os.listdir(folder_path):
            if filename.lower().endswith(ALLOWED_EXTENSIONS):
                image_files.append(os.path.join(folder_path, filename))

    elif mode == "dialog":
        files, _ = QFileDialog.getOpenFileNames(
            parent,
            caption="Wybierz pliki graficzne",
            filter="Pliki graficzne (*.png *.jpg *.jpeg *.bmp *.gif *.webp)"
        )
        image_files = files or []

    print(f"Wczytano {len(image_files)} plików ({mode}).")
    return image_files

# wczytaj obrazy z folderu i wyswietl w panelu
def display_images_in_panel(panel_widget, image_paths, on_image_select=None, max_preview_size=(150, 150), clear=True):
    panel_layout = panel_widget.layout()
    if panel_layout is None:
        panel_layout = QVBoxLayout(panel_widget)

    if clear:
        # Wyczyść poprzednią zawartość tylko jeśli clear == True
        while panel_layout.count():
            child = panel_layout.takeAt(0)
            if child.widget():
                child.widget().setParent(None)

    thumbnail_labels = []

    for idx, path in enumerate(image_paths):
        pixmap = QPixmap(path)
        if pixmap.isNull():
            continue
        pixmap = pixmap.scaled(*max_preview_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        label = QLabel()
        label.setPixmap(pixmap)
        label.setAlignment(Qt.AlignCenter)
        label.setCursor(Qt.PointingHandCursor)

        if on_image_select:
            label.mousePressEvent = lambda e, i=idx: on_image_select(i)

        panel_layout.addWidget(label)
        thumbnail_labels.append(label)

    return thumbnail_labels


def set_active_image(index, image_paths, label, main_image_label, thumbnails, set_zoom_level, update_zoom_display=None):
    if 0 <= index < len(image_paths):
        set_zoom_level(1.0)  # reset zoom
        pixmap = QPixmap(image_paths[index])
        label.setPixmap(pixmap)
        label.setAlignment(Qt.AlignCenter)

        for i, thumb in enumerate(thumbnails):
            thumb.setStyleSheet("border: 2px solid #3d74f0;" if i == index else "border: none;")

        if update_zoom_display:
            update_zoom_display()

def display_scaled_image(pixmap, label, zoom_level):
    if pixmap.isNull():
        return

    target_size = label.size() * zoom_level
    scaled = pixmap.scaled(target_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
    label.setPixmap(scaled)


def handle_scroll(event, is_ctrl, current_index, image_paths, zoom_level, zoom_callback, image_callback):
    if is_ctrl:
        delta = event.angleDelta().y()
        zoom_level = zoom_level * (1.1 if delta > 0 else 1 / 1.1)
        zoom_level = max(0.1, min(zoom_level, 10.0))
        zoom_callback(zoom_level)
        return zoom_level, current_index

    delta = event.angleDelta().y()
    if delta > 0:
        new_index = max(0, current_index - 1)
    else:
        new_index = min(len(image_paths) - 1, current_index + 1)

    if new_index != current_index:
        image_callback(new_index)
    return zoom_level, new_index

def handle_mouse_press(event, zoom_level):
    if event.button() == Qt.LeftButton and zoom_level > 1.0:
        return True, event.pos()
    return False, None

def handle_mouse_move(event, is_dragging, drag_start_pos, scroll_offset, zoom_level):
    if is_dragging and zoom_level > 1.0:
        delta = event.pos() - drag_start_pos
        new_offset = scroll_offset + delta
        return True, event.pos(), new_offset
    return False, drag_start_pos, scroll_offset

def handle_mouse_release(event):
    if event.button() == Qt.LeftButton:
        return False  # dragging ends
    return True

def draw_boxes_on_pixmap(pixmap, boxes):
    result = QPixmap(pixmap.size())
    result.fill(Qt.transparent)

    painter = QPainter(result)
    painter.drawPixmap(0, 0, pixmap)
    pen = QPen(QColor(255, 0, 0), 3)
    painter.setPen(pen)

    for rect in boxes:
        painter.drawRect(rect)

    painter.end()
    return result

from PySide6.QtCore import QRect

# wczytaj bounding boxy
def load_bounding_boxes_from_txt(file_path):
    boxes = []
    try:
        with open(file_path, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) == 5:
                    try:
                        xmin = int(float(parts[1]))
                        ymin = int(float(parts[2]))
                        xmax = int(float(parts[3]))
                        ymax = int(float(parts[4]))
                        w = xmax - xmin
                        h = ymax - ymin
                        boxes.append(QRect(xmin, ymin, w, h))
                    except ValueError:
                        continue
    except FileNotFoundError:
        print(f"[!] Nie znaleziono pliku: {file_path}")
    return boxes

# odswiez liste plikow w panelu bocznym
def refresh_file_list_in_sidebar(window):

    window.sidebar_file_list.clear()

    for path in window.image_paths:
        filename = os.path.basename(path)
        window.sidebar_file_list.addItem(filename)

# usun zaznaczone obrazy z listy i z panelu miniatur
def delete_selected_images(window):
    selected_items = window.sidebar_file_list.selectedItems()

    if not selected_items:
        window.image_paths.clear()
    else:
        selected_filenames = {item.text() for item in selected_items}
        window.image_paths = [
            path for path in window.image_paths
            if os.path.basename(path) not in selected_filenames
        ]

    refresh_file_list_in_sidebar(window)

    # odswiez podglad miniatur w prawym panelu
    window.right_thumbnails = display_images_in_panel(
        window.right_scroll_content,
        window.image_paths,
        on_image_select=window.set_active_image
    )

    # zresetuj srodkowy panel
    window.main_image_label.clear()
    window.current_image_index = -1
    window.current_pixmap = QPixmap()
    window.zoom_level = 1.0

