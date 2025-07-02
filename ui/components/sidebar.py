# foxchat/ui/components/sidebar.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QListWidget,
    QComboBox, QSizePolicy
)
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QFont

from core.utils import load_icon


class Sidebar(QWidget):
    """
    Sidebar widget:
    - Lists chat sessions and API profiles.
    - Contains buttons for new sessions, adding APIs, and settings.
    - Switches between AI Chat and Anonymous Chat modes.
    """

    def __init__(self):
        super().__init__()
        self.setObjectName("Sidebar")
        self.setAcceptDrops(False)  # Just to be explicit
        self.setMinimumWidth(0)
        self.setMaximumWidth(260)
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        # --- Chat Sessions ---
        sessions_title = QLabel("Chat Sessions")
        sessions_title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        layout.addWidget(sessions_title)

        self.session_list = QListWidget()
        self.session_list.setEditTriggers(
            QListWidget.EditTrigger.DoubleClicked |
            QListWidget.EditTrigger.SelectedClicked
        )
        layout.addWidget(self.session_list)

        self.btn_new_session = QPushButton("+ New Chat")
        self.btn_new_session.setCursor(Qt.CursorShape.PointingHandCursor)
        layout.addWidget(self.btn_new_session)

        self.chat_mode_switch = QComboBox()
        self.chat_mode_switch.addItems(["AI Chat", "Anonymous Chat"])
        self.chat_mode_switch.setCursor(Qt.CursorShape.PointingHandCursor)
        layout.addWidget(self.chat_mode_switch)

        # --- API Section ---
        api_label = QLabel("API Profiles")
        api_label.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        layout.addWidget(api_label)

        self.api_list = QListWidget()
        layout.addWidget(self.api_list)

        self.btn_add_api = QPushButton("Add Custom API")
        self.btn_add_api.setIcon(load_icon("Add.png"))
        self.btn_add_api.setIconSize(QSize(20, 20))
        self.btn_add_api.setObjectName("IconButton")
        self.btn_add_api.setCursor(Qt.CursorShape.PointingHandCursor)
        layout.addWidget(self.btn_add_api)

        # --- Settings ---
        self.btn_settings = QPushButton("Settings")
        self.btn_settings.setIcon(load_icon("Cog.png"))
        self.btn_settings.setIconSize(QSize(20, 20))
        self.btn_settings.setObjectName("IconButton")
        self.btn_settings.setCursor(Qt.CursorShape.PointingHandCursor)
        layout.addWidget(self.btn_settings)

        # --- Push everything up ---
        layout.addStretch()
