# foxchat/ui/chat_area.py

import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QScrollArea, QLabel, QFrame
)
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QPixmap, QCursor, QDesktopServices, QFont

from ui.message_bubble import MessageBubble
from advanced.markdown_renderer import render_markdown
from advanced.file_preview_widget import is_image_file


class ChatArea(QWidget):
    """
    ChatArea widget:
    Contains a scrollable area with vertical stacked messages.
    """

    def __init__(self):
        super().__init__()

        # --- Layout setup ---
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        layout.addWidget(self.scroll_area)

        self.chat_widget = QWidget()
        self.chat_layout = QVBoxLayout(self.chat_widget)
        self.chat_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.chat_layout.setSpacing(15)
        self.chat_layout.setContentsMargins(15, 15, 15, 15)

        self.scroll_area.setWidget(self.chat_widget)

    def clear_messages(self):
        """Remove all message widgets."""
        while self.chat_layout.count():
            child = self.chat_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def scroll_to_bottom(self):
        """Scrolls to the bottom."""
        # Use QTimer to ensure scrolling happens after layout is updated
        from PyQt6.QtCore import QTimer
        # First scroll with a short delay
        QTimer.singleShot(10, lambda: self.scroll_area.verticalScrollBar().setValue(
            self.scroll_area.verticalScrollBar().maximum()
        ))
        # Second scroll with a longer delay to ensure we reach the absolute bottom
        QTimer.singleShot(100, lambda: self.scroll_area.verticalScrollBar().setValue(
            self.scroll_area.verticalScrollBar().maximum()
        ))

    def add_message(self, content, is_user=True, sender=None):
        """
        Adds a message to the chat.
        Supports [Uploaded File: path] tags for file previews.
        """
        # Ensure we're at the bottom if we were already scrolled to bottom
        scrollbar = self.scroll_area.verticalScrollBar()
        was_at_bottom = scrollbar.value() >= scrollbar.maximum() - 10

        # --- Optional sender label ---
        if sender:
            sender_label = QLabel(sender)
            sender_label.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
            sender_label.setStyleSheet("color: gray;")
            sender_label.setAlignment(Qt.AlignmentFlag.AlignRight if is_user else Qt.AlignmentFlag.AlignLeft)
            self.chat_layout.addWidget(sender_label)

        # --- Create message frame ---
        message_frame = QFrame()
        message_layout = QVBoxLayout(message_frame)
        message_layout.setContentsMargins(10, 5, 10, 5)
        message_layout.setSpacing(5)
        message_frame.setObjectName("UserBubble" if is_user else "BotBubble")

        text_lines, file_paths = self._split_content(content)

        # --- Text part (Markdown) ---
        if text_lines:
            markdown_html = render_markdown("\n".join(text_lines))
            text_label = QLabel()
            text_label.setText(markdown_html)
            text_label.setWordWrap(True)
            text_label.setTextFormat(Qt.TextFormat.RichText)
            text_label.setOpenExternalLinks(True)
            message_layout.addWidget(text_label)

        # --- File previews ---
        for path in file_paths:
            self._add_file_preview(message_layout, path)

        # --- Add to main chat layout ---
        self.chat_layout.addWidget(
            message_frame,
            alignment=Qt.AlignmentFlag.AlignRight if is_user else Qt.AlignmentFlag.AlignLeft
        )

        # Only scroll to bottom if we were already at the bottom or this is a user message
        if was_at_bottom or is_user:
            self.scroll_to_bottom()

    def _split_content(self, content):
        """Split message content into text lines and file paths."""
        file_lines = []
        text_lines = []

        for line in content.strip().splitlines():
            if line.startswith("[Uploaded File: ") and line.endswith("]"):
                file_path = line[len("[Uploaded File: "):-1]
                file_lines.append(file_path)
            else:
                text_lines.append(line)

        return text_lines, file_lines

    def _add_file_preview(self, layout, filepath):
        """Add file preview or file label to the layout."""
        if not os.path.exists(filepath):
            layout.addWidget(QLabel(f"❓ Missing: {os.path.basename(filepath)}"))
            return

        if is_image_file(filepath):
            pixmap = QPixmap(filepath).scaledToWidth(300, Qt.TransformationMode.SmoothTransformation)
            label = QLabel()
            label.setPixmap(pixmap)
            label.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        else:
            label = QLabel(f"📄 {os.path.basename(filepath)}")
            label.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        label.mousePressEvent = lambda e, p=filepath: self._open_file(p, e)
        layout.addWidget(label)

    def _open_file(self, filepath, event):
        """Open file in default OS handler."""
        if os.path.exists(filepath):
            QDesktopServices.openUrl(QUrl.fromLocalFile(filepath))
