# foxchat/ui/message_bubble.py

from PyQt6.QtWidgets import QFrame, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt
from advanced.markdown_renderer import render_markdown


class MessageBubble(QFrame):
    def __init__(self, text: str, is_user: bool, sender: str = ""):
        super().__init__()
        self.setObjectName("MessageBubble")

        # --- Style ---
        bg_color = "#DCF8C6" if is_user else "#F1F0F0"
        self.setStyleSheet(f"""
        QFrame#MessageBubble {{
            border: 1px solid #ccc;
            border-radius: 10px;
            background-color: {bg_color};
            padding: 8px;
        }}
        """)

        # --- Layout ---
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(4)

        # Optional sender label (for AI name / You)
        if sender:
            sender_label = QLabel(sender)
            sender_label.setStyleSheet("font-weight: bold; color: #444;")
            layout.addWidget(sender_label)

        # Markdown-rendered message content
        content = QLabel()
        content.setTextFormat(Qt.TextFormat.RichText)
        content.setText(render_markdown(text))  # Use actual markdown renderer
        content.setWordWrap(True)
        layout.addWidget(content)
