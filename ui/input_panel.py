# foxchat/ui/input_panel.py

from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QPushButton, QTextEdit,
    QVBoxLayout, QFrame
)
from PyQt6.QtGui import QKeyEvent, QDragEnterEvent, QDropEvent
from PyQt6.QtCore import QSize, Qt, pyqtSignal
import os
import functools

from advanced.file_preview_widget import FilePreviewWidget
from core.utils import load_icon


class InputTextBox(QTextEdit):
    send_requested = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setPlaceholderText("Type your message here...")
        self.setMinimumHeight(48)
        self.setMaximumHeight(120)
        self.setAcceptRichText(False)
        self.setTabChangesFocus(True)
        self.setAcceptDrops(False)  # Disable default drop behavior

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            if event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
                super().keyPressEvent(event)
            else:
                self.send_requested.emit()
        else:
            super().keyPressEvent(event)

    def dragEnterEvent(self, event: QDragEnterEvent):
        self.parent().dragEnterEvent(event)

    def dropEvent(self, event: QDropEvent):
        self.parent().dropEvent(event)


class InputPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 10, 20, 15)
        main_layout.setSpacing(5)

        # --- File Previews ---
        self.preview_frame = QFrame()
        self.preview_frame.setObjectName("FilePreviewFrame")
        self.preview_layout = QHBoxLayout(self.preview_frame)
        self.preview_layout.setContentsMargins(5, 5, 5, 5)
        self.preview_layout.setSpacing(10)
        self.preview_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.preview_frame.setVisible(False)
        main_layout.addWidget(self.preview_frame)

        # --- Input Area ---
        input_layout = QHBoxLayout()
        input_layout.setSpacing(10)
        input_layout.setContentsMargins(0, 0, 0, 0)

        self.text_input = InputTextBox()
        input_layout.addWidget(self.text_input)

        self.btn_send = QPushButton()
        self.btn_send.setIcon(load_icon("send.png"))
        self.btn_send.setIconSize(QSize(28, 28))
        self.btn_send.setFixedSize(56, 48)
        self.btn_send.setObjectName("SendButton")
        self.btn_send.setCursor(Qt.CursorShape.PointingHandCursor)
        input_layout.addWidget(self.btn_send)

        self.btn_upload = QPushButton()
        self.btn_upload.setIcon(load_icon("Upload.png"))
        self.btn_upload.setIconSize(QSize(28, 28))
        self.btn_upload.setFixedSize(56, 48)
        self.btn_upload.setObjectName("UploadButton")
        self.btn_upload.setCursor(Qt.CursorShape.PointingHandCursor)
        input_layout.addWidget(self.btn_upload)

        main_layout.addLayout(input_layout)

        self.text_input.send_requested.connect(self.btn_send.click)
        self.pending_files = []

    # --- File Preview Methods ---
    def add_file_preview(self, filepath):
        if filepath in self.pending_files:
            return  # Avoid duplicates
        preview = FilePreviewWidget(filepath)
        preview.remove_requested.connect(functools.partial(self.remove_file_preview, preview))
        self.preview_layout.addWidget(preview)
        self.pending_files.append(filepath)
        self.preview_frame.setVisible(True)

    def remove_file_preview(self, widget):
        if widget.filepath in self.pending_files:
            self.pending_files.remove(widget.filepath)
        self.preview_layout.removeWidget(widget)
        widget.deleteLater()
        if not self.pending_files:
            self.preview_frame.setVisible(False)

    def get_attached_files(self):
        return list(self.pending_files)

    def clear_file_previews(self):
        for i in reversed(range(self.preview_layout.count())):
            widget = self.preview_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
                widget.deleteLater()
        self.pending_files.clear()
        self.preview_frame.setVisible(False)

    # --- Drag & Drop ---
    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                if url.isLocalFile() and os.path.isfile(url.toLocalFile()):
                    event.acceptProposedAction()
                    return
        event.ignore()

    def dropEvent(self, event: QDropEvent):
        if event.mimeData().hasUrls():
            added_any = False
            for url in event.mimeData().urls():
                if url.isLocalFile():
                    path = url.toLocalFile()
                    if os.path.isfile(path):
                        self.add_file_preview(path)
                        added_any = True
            if added_any:
                event.acceptProposedAction()
            else:
                event.ignore()
        else:
            event.ignore()
