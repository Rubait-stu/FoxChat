from PyQt6.QtWidgets import QLabel, QVBoxLayout, QFrame
from PyQt6.QtCore import Qt, pyqtSignal, QUrl
from PyQt6.QtGui import QPixmap, QFont, QDesktopServices, QCursor, QMouseEvent, QDragEnterEvent, QDropEvent
import os
from core.utils import load_icon

def is_image_file(path: str) -> bool:
    ext = os.path.splitext(path)[-1].lower()
    return ext in ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp']

class ClickableLabel(QLabel):
    clicked = pyqtSignal()

    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setStyleSheet("background: transparent;")

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)


class FilePreviewWidget(QFrame):
    # Signal definitions
    remove_requested = pyqtSignal()
    file_dropped = pyqtSignal(str)

    FILETYPE_ICONS = {
        '.pdf': 'pdf.png',
        '.xls': 'xls.png',
        '.xlsx': 'xls.png',
        '.txt': 'txt.png',
        '.doc': 'doc.png',
        '.docx': 'doc.png',
        '.ppt': 'ppt.png',
        '.pptx': 'ppt.png',
        '.csv': 'csv.png',
        '.zip': 'zip.png',
    }

    FILETYPE_EMOJIS = {
        '.pdf': "📄",
        '.xls': "📊",
        '.txt': "📝",
        '.doc': "📃",
        '.ppt': "📽️",
        '.csv': "📈",
        '.zip': "🗜️",
        'default': "📁",
    }

    IMAGE_DISPLAY_SIZE = 80
    ICON_DISPLAY_SIZE = 48

    def __init__(self, path: str, on_cancel=None):
        super().__init__()
        self.filepath = path
        self.on_cancel_callback = on_cancel

        self.setObjectName("FilePreviewWidget")
        self.setStyleSheet("""
            QFrame#FilePreviewWidget {
                border: 1px solid #ccc;
                border-radius: 6px;
                background-color: #f0f0f0;
            }
            QLabel#CloseButton {
                color: red;
                font-size: 16px;
                background-color: transparent;
                border-radius: 10px;
                padding: 0px 4px;
            }
            QLabel#CloseButton:hover {
                color: darkred;
                background-color: rgba(255, 255, 255, 150);
            }
        """)

        self.setAcceptDrops(True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(3)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.image_label = QLabel()
        self.image_label.setFont(QFont("Segoe UI", 10))
        self.image_label.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.filename_label = QLabel(os.path.basename(path))
        self.filename_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.filename_label.setFont(QFont("Segoe UI", 9))
        self.filename_label.setStyleSheet("color: #333;")
        self.filename_label.setWordWrap(True)
        self.filename_label.setMaximumWidth(self.IMAGE_DISPLAY_SIZE * 2)

        self._populate_preview(path)

        self.image_label.mousePressEvent = self.open_file
        layout.addWidget(self.image_label)
        layout.addWidget(self.filename_label)

        self.close_btn = ClickableLabel("❌", self)
        self.close_btn.setObjectName("CloseButton")
        self.close_btn.setFixedSize(20, 20)
        self.close_btn.setToolTip("Remove this file")
        self.close_btn.clicked.connect(self._on_close_clicked)
        self.close_btn.raise_()

    def _populate_preview(self, path: str):
        if is_image_file(path):
            # image logic unchanged
            pixmap = QPixmap(path)
            if pixmap.isNull():
                self.image_label.setText("❌ Invalid image")
                self.image_label.setFixedSize(self.IMAGE_DISPLAY_SIZE, self.IMAGE_DISPLAY_SIZE)
            else:
                scaled = pixmap.scaled(
                    self.IMAGE_DISPLAY_SIZE, self.IMAGE_DISPLAY_SIZE,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                self.image_label.setPixmap(scaled)
                self.image_label.setFixedSize(scaled.size())
        else:
            ext = os.path.splitext(path)[-1].lower()
            icon_name = self.FILETYPE_ICONS.get(ext)
            if icon_name:
                icon = load_icon(icon_name)
                pixmap = icon.pixmap(self.ICON_DISPLAY_SIZE, self.ICON_DISPLAY_SIZE)
                if not pixmap.isNull():
                    self.image_label.setPixmap(pixmap)
                    self.image_label.setFixedSize(pixmap.size())
                    return

            emoji = self.FILETYPE_EMOJIS.get(ext, self.FILETYPE_EMOJIS['default'])
            self.image_label.setText(emoji)
            self.image_label.setFixedSize(self.ICON_DISPLAY_SIZE, self.ICON_DISPLAY_SIZE)

    def resizeEvent(self, event):
        self.close_btn.move(self.width() - self.close_btn.width() - 6, 6)
        super().resizeEvent(event)

    def _on_close_clicked(self):
        self.remove_requested.emit()
        if self.on_cancel_callback:
            self.on_cancel_callback(self)

    def open_file(self, event):
        if os.path.exists(self.filepath):
            QDesktopServices.openUrl(QUrl.fromLocalFile(self.filepath))
        else:
            print(f"⚠️ File not found: {self.filepath}")

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                if url.isLocalFile():
                    event.acceptProposedAction()
                    return
        event.ignore()

    def dropEvent(self, event: QDropEvent):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                if url.isLocalFile():
                    self.file_dropped.emit(url.toLocalFile())
            event.acceptProposedAction()
        else:
            event.ignore()
