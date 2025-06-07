import sys
from PIL import Image, ImageDraw
from PySide6.QtPrintSupport import QPrinter
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QToolButton,
    QHBoxLayout, QFrame, QSizePolicy, QLabel, QScrollArea, QFileDialog,
    QListWidget, QAbstractItemView, QListWidgetItem
)
from PySide6.QtCore import Qt, QSize, QEvent, QPoint, QSizeF, QRectF, QRect
from PySide6.QtGui import QIcon, QFontMetrics, QPainter, QPageLayout, QPixmap, QPainterPath
from handlers import *
from detect import detect_bounding_boxes_batch

class CustomTitleBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setObjectName("CustomTitleBar")
        self.setFixedHeight(40)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 10, 0)
        layout.setSpacing(8)

        self.title = QLabel("Styled Dashboard", self)
        self.title.setStyleSheet("color: #d09dd6; font-weight: bold;")
        layout.addWidget(self.title)
        layout.addStretch()

        # Minimize, Maximize/Restore, Close buttons
        btn_min = QToolButton(self)
        btn_min.setIcon(QIcon("assets/icons/minimize.png"))
        btn_min.setIconSize(QSize(20, 20))
        btn_min.setStyleSheet("background: transparent; border: none;")
        btn_min.clicked.connect(self.window().showMinimized)
        layout.addWidget(btn_min)

        self.btn_max = QToolButton(self)
        self.btn_max.setIcon(QIcon("assets/icons/maximize.png"))
        self.btn_max.setIconSize(QSize(20, 20))
        self.btn_max.setStyleSheet("background: transparent; border: none;")
        self.btn_max.clicked.connect(self.toggle_max_restore)
        layout.addWidget(self.btn_max)

        btn_close = QToolButton(self)
        btn_close.setIcon(QIcon("assets/icons/close.png"))
        btn_close.setIconSize(QSize(20, 20))
        btn_close.setStyleSheet("background: transparent; border: none;")
        btn_close.clicked.connect(self.window().close)
        layout.addWidget(btn_close)

        self._drag_pos = None

    def toggle_max_restore(self):
        win = self.window()
        if win.isMaximized():
            win.showNormal()
            self.btn_max.setIcon(QIcon("assets/icons/maximize.png"))
        else:
            win.showMaximized()
            self.btn_max.setIcon(QIcon("assets/icons/maximize.png"))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.window().frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self._drag_pos and event.buttons() == Qt.LeftButton:
            self.window().move(event.globalPosition().toPoint() - self._drag_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        self._drag_pos = None

# function to define the main window of the application
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Równowaga - app")
        self.setMinimumSize(1280, 720)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.init_ui()
        self.current_image_index = -1
        self.image_paths = []
        self.right_thumbnails = []
        self.current_pixmap = QPixmap()
        self.zoom_level = 1.0
        self.current_boxes = []
        self.boxes_by_path = {}
        self.show_boxes = True
        self.setWindowFlag(Qt.FramelessWindowHint)


    def eventFilter(self, obj, event):
        if event.type() == QEvent.Wheel and obj in (self.right_scroll_content, self.main_image_label):
            if not self.image_paths:
                return False

            is_ctrl_pressed = QApplication.keyboardModifiers() == Qt.ControlModifier
            delta = event.angleDelta().y()

            if is_ctrl_pressed:
                # Pozycja kursora wzgledem QLabel
                cursor_pos = event.position().toPoint()
                label_pos = self.main_image_label.pos()
                cursor_offset = cursor_pos - label_pos

                # Proporcja kursora wzgledem obrazu
                if not self.main_image_label.pixmap():
                    return True

                pixmap_size = self.main_image_label.pixmap().size()
                if pixmap_size.width() == 0 or pixmap_size.height() == 0:
                    return True

                rel_x = cursor_offset.x() / pixmap_size.width()
                rel_y = cursor_offset.y() / pixmap_size.height()

                # Zmiana zoomu
                old_zoom = self.zoom_level
                if delta > 0:
                    self.zoom_level *= 1.1
                else:
                    self.zoom_level /= 1.1
                self.zoom_level = max(0.1, min(self.zoom_level, 10.0))

                # Nowy rozmiar i offset
                new_pixmap_size = self.current_pixmap.size() * self.zoom_level
                dx = cursor_pos.x() - new_pixmap_size.width() * rel_x
                dy = cursor_pos.y() - new_pixmap_size.height() * rel_y
                self._scroll_offset = QPoint(int(dx), int(dy))

                self.display_scaled_image()
                return True
            else:
                if delta > 0:
                    new_index = max(0, self.current_image_index - 1)
                else:
                    new_index = min(len(self.image_paths) - 1, self.current_image_index + 1)

                if new_index != self.current_image_index:
                    self.set_active_image(new_index)

            return True

        return super().eventFilter(obj, event)

    # function to load images from disk and display them in the right panel
    def load_and_display_images(self):
        new_paths = get_image_paths(mode="dialog", parent=self)
        if not new_paths:
            return

        unique_new_paths = [p for p in new_paths if p not in self.image_paths]
        if not unique_new_paths:
            print("Brak nowych plików do dodania.")
            return

        self.image_paths.extend(unique_new_paths)

        # Dodaj tylko nowe miniatury bez czyszczenia
        new_thumbnails = display_images_in_panel(
            self.right_scroll_content,
            unique_new_paths,
            on_image_select=self.set_active_image,
            clear=False  # <== kluczowa zmiana
        )
        self.right_thumbnails.extend(new_thumbnails)

        refresh_file_list_in_sidebar(self)

    # function to choose image from list and display it in main preview panel
    def set_active_image(self, index):
        if 0 <= index < len(self.image_paths):
            self.current_image_index = index
            path = self.image_paths[index]
            self.current_pixmap = QPixmap(path)
            self.zoom_level = 1.0  # reset zoom
            self.display_scaled_image()

            for i, label in enumerate(self.right_thumbnails):
                if i == index:
                    label.setStyleSheet("border: 2px solid #3d74f0;")
                else:
                    label.setStyleSheet("border: none;")

    # reset view to default state
    def reset_view(self):
        self.zoom_level = 1.0
        self._scroll_offset = QPoint(0, 0)
        self.display_scaled_image()

    # function to analyze images and apply bounding boxes on images
    def analyze_and_apply_boxes(self):
        if not self.image_paths:
            print("Brak obrazów do analizy.")
            return

        print(f"[AI] Analiza {len(self.image_paths)} obrazów...")
        results = detect_bounding_boxes_batch(self.image_paths)

        for index, path in enumerate(self.image_paths):
            boxes_data = results.get(path, [])
            rects = [QRect(x, y, w, h) for (x, y, w, h) in boxes_data]
            self.boxes_by_path[path] = rects
            print(f"  - {os.path.basename(path)}: {len(rects)} obiektów")

            if index == self.current_image_index:
                self.current_boxes = rects

        self.display_scaled_image()

    def save_images_with_boxes_to_pdf(self):
        if not self.image_paths:
            print("Brak załadowanych obrazów.")
            return

        save_path, _ = QFileDialog.getSaveFileName(self, "Zapisz PDF", "", "PDF Files (*.pdf)")
        if not save_path:
            return

        margin = 20
        images_list = []
        total_height = 0
        max_width = 0

        for path in self.image_paths:
            try:
                img = Image.open(path).convert("RGB")
                draw = ImageDraw.Draw(img)

                boxes = self.boxes_by_path.get(path, [])

                for rect in boxes:
                    x, y, w, h = rect.x(), rect.y(), rect.width(), rect.height()
                    draw.rectangle([x, y, x + w, y + h], outline="red", width=3)

                images_list.append(img)
                total_height += img.height + margin
                max_width = max(max_width, img.width)
            except Exception as e:
                print(f"Błąd ładowania obrazu {path}:", e)

        if not images_list:
            print("Brak obrazów do zapisania.")
            return

        total_height -= margin

        combined_image = Image.new("RGB", (max_width, total_height), "black")
        y_offset = 0
        for img in images_list:
            x_offset = (max_width - img.width) // 2
            combined_image.paste(img, (x_offset, y_offset))
            y_offset += img.height + margin

        try:
            combined_image.save(save_path, "PDF", resolution=100.0)
            print(f"[✓] PDF zapisany: {save_path}")
        except Exception as e:
            print("Błąd zapisu PDF:", e)


    def toggle_bounding_boxes(self):
        self.show_boxes = not self.show_boxes

        # Zmień ikonę przycisku
        icon_path = "assets/icons/bbox_show.png" if self.show_boxes else "assets/icons/bbox_hide.png"
        self.sidebar_toggle_button.setIcon(QIcon(icon_path))

        # Przerysuj aktualny obraz
        self.display_scaled_image()

    # main function to initialize the ui components
    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Root layout (vertical)
        self.root_layout = QVBoxLayout(central_widget)
        self.root_layout.setContentsMargins(0, 0, 0, 0)
        self.root_layout.setSpacing(0)

        # Custom title bar
        self.title_bar = CustomTitleBar(self)
        self.root_layout.addWidget(self.title_bar)

        # Main content layout (horizontal)
        self.content_layout = QHBoxLayout()
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(0)

        # --- Sidebar ---
        self.sidebar = QFrame()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setAlignment(Qt.AlignTop)

        # Top-left 3 buttons
        btn_row = QHBoxLayout()
        for i in range(3):
            btn = QPushButton()
            btn.setIcon(QIcon(f"assets/icons/button_{i + 1}.png"))
            btn.setIconSize(QSize(24, 24))
            btn.setObjectName("SidebarTopButton")
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

            if i == 0:
                btn.clicked.connect(self.load_and_display_images)
            elif i == 1:
                btn.clicked.connect(lambda: delete_selected_images(self))
            elif i == 2:
                btn.clicked.connect(self.toggle_bounding_boxes)
                self.sidebar_toggle_button = btn
                btn.setIcon(QIcon("assets/icons/bbox_show.png"))

            btn_row.addWidget(btn)
        self.sidebar_layout.addLayout(btn_row)

        # Text area below buttons
        self.sidebar_label = QLabel("Tu będzie opis lub tekst")
        self.sidebar_label.setObjectName("SidebarLabel")
        self.sidebar_label.setWordWrap(True)
        self.sidebar_label.setMinimumHeight(60)
        self.sidebar_layout.addWidget(self.sidebar_label)

        # Scrollable file list
        self.sidebar_file_list = QListWidget()
        self.sidebar_file_list.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.sidebar_file_list.setObjectName("SidebarFileList")
        self.sidebar_layout.addWidget(self.sidebar_file_list)

        # --- Center preview panel ---
        self.preview_panel = QFrame()
        self.preview_panel.setObjectName("PreviewPanel")
        self.preview_panel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.main_image_label = QLabel(self.preview_panel)
        self.main_image_label.setAlignment(Qt.AlignCenter)
        self.main_image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.main_image_label.setScaledContents(False)

        self.preview_panel.setLayout(None)
        self.main_image_label.move(0, 0)
        self.main_image_label.resize(self.preview_panel.size())

        # --- Right panel ---
        self.right_panel = QFrame()
        self.right_panel.setObjectName("RightPanel")
        self.right_panel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.right_panel.setContentsMargins(0, 0, 0, 0)
        scroll_area = QScrollArea(self.right_panel)

        self.right_scroll_content = QWidget()
        self.right_scroll_content.setObjectName("RightPanel")
        self.right_scroll_content.setLayout(QVBoxLayout())
        scroll_area.setWidget(self.right_scroll_content)
        scroll_area.setWidgetResizable(True)

        layout = QVBoxLayout(self.right_panel)
        layout.addWidget(scroll_area)

        # --- Bottom overlay ---
        self.bottom_panel = QFrame(self.preview_panel)
        self.bottom_panel.setObjectName("BottomOverlay")
        self.bottom_panel_layout = QHBoxLayout(self.bottom_panel)
        self.bottom_panel_layout.setContentsMargins(10, 10, 10, 10)

        self.bottom_buttons = []
        icons = ["reset.png", "bbox.png", "pdf.png"]
        handlers = [self.reset_view, self.analyze_and_apply_boxes, self.save_images_with_boxes_to_pdf]

        for icon_filename, handler in zip(icons, handlers):
            btn = QPushButton()
            btn.setIcon(QIcon(f"assets/icons/{icon_filename}"))
            btn.setIconSize(QSize(32, 32))
            btn.setObjectName("OverlayButton")
            btn.clicked.connect(handler)
            self.bottom_buttons.append(btn)
            self.bottom_panel_layout.addWidget(btn)

        self.bottom_panel.setParent(self.preview_panel)
        self.bottom_panel.raise_()

        # --- Add panels to content layout ---
        self.content_layout.addWidget(self.sidebar)
        self.content_layout.addWidget(self.preview_panel)
        self.content_layout.addWidget(self.right_panel)

        # --- Add content layout to root layout ---
        self.root_layout.addLayout(self.content_layout)

        # --- Event filters and drag support ---
        self.right_scroll_content.installEventFilter(self)
        self.main_image_label.installEventFilter(self)
        self.preview_panel.installEventFilter(self)
        self._is_dragging = False
        self._drag_start_pos = None
        self._scroll_offset = QPoint(0, 0)

    # event handlers for mouse and scroll events
    def mousePressEvent(self, event):
        self._is_dragging, self._drag_start_pos = handle_mouse_press(event, self.zoom_level)
        if self._is_dragging:
            self.setCursor(Qt.ClosedHandCursor)

    def mouseMoveEvent(self, event):
        moved, new_start, new_offset = handle_mouse_move(
            event,
            self._is_dragging,
            self._drag_start_pos,
            self._scroll_offset,
            self.zoom_level
        )
        if moved:
            self._drag_start_pos = new_start
            self._scroll_offset = new_offset
            self.update_image_position()

    def mouseReleaseEvent(self, event):
        self._is_dragging = handle_mouse_release(event)
        self.setCursor(Qt.ArrowCursor)

    # update image position based on zoom level and scroll offset
    def update_image_position(self):
        if self.zoom_level <= 1.01:
            # Wyśrodkuj
            panel_size = self.preview_panel.size()
            image_size = self.main_image_label.size()
            x = (panel_size.width() - image_size.width()) // 2
            y = (panel_size.height() - image_size.height()) // 2
            self.main_image_label.move(max(0, x), max(0, y))
        else:
            self.main_image_label.move(self._scroll_offset)
    def resizeEvent(self, event):
        width = self.width()

        # Responsywne szerokości
        sidebar_width = int(width * 0.20)
        right_width = int(width * 0.14)
        center_width = width - sidebar_width - right_width

        self.sidebar.setFixedWidth(sidebar_width)
        self.right_panel.setFixedWidth(right_width)

        # Bottom panel (overlay)
        center_height = self.preview_panel.height()
        overlay_height = 80
        overlay_width = int(center_width * 0.3)

        self.bottom_panel.setFixedSize(overlay_width, overlay_height)
        self.bottom_panel.move(
            (center_width - overlay_width) // 2,
            center_height - overlay_height + 10
        )

        self.main_image_label.resize(self.preview_panel.size())
        self.display_scaled_image()
        super().resizeEvent(event)

    def set_zoom_level_and_refresh(self, zl):
        self.zoom_level = zl
        self.display_scaled_image()

    # display scaled image with bounding boxes
    def display_scaled_image(self):
        if self.current_pixmap.isNull():
            return

        # Bazuj na oryginalnym pixmap
        scaled_size = self.current_pixmap.size() * self.zoom_level
        scaled = self.current_pixmap.scaled(
            scaled_size,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )

        if self.show_boxes:
            image_path = self.image_paths[self.current_image_index]
            boxes = self.boxes_by_path.get(image_path, [])
            if boxes:
                boxed = QPixmap(scaled)  # zrób kopię, żeby nie nadpisać oryginału
                painter = QPainter(boxed)
                pen = QPen(QColor("red"))
                pen.setWidth(2)
                painter.setPen(pen)

                scale_ratio = self.zoom_level
                for rect in boxes:
                    scaled_rect = QRectF(
                        rect.x() * scale_ratio,
                        rect.y() * scale_ratio,
                        rect.width() * scale_ratio,
                        rect.height() * scale_ratio
                    )
                    painter.drawRect(scaled_rect)

                painter.end()
                scaled = boxed  # zamień tylko jeśli rysowaliśmy

        self.main_image_label.setPixmap(scaled)
        self.main_image_label.resize(scaled.size())

        if self.zoom_level <= 1.01:
            self._scroll_offset = QPoint(0, 0)

        self.update_image_position()

    def paintEvent(self, event):
        path = QPainterPath()
        radius = 16
        path.addRoundedRect(self.rect(), radius, radius)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setClipPath(path)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor("#1e161f"))
        painter.drawPath(path)
        super().paintEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    with open("style.qss", "r") as f:
        app.setStyleSheet(f.read())
    window.show()
    window.resizeEvent(None)
    sys.exit(app.exec())
