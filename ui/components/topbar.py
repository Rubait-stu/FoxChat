# foxchat/ui/components/topbar.py

"""
TopBar widget for FoxChat.

Includes:
- App logo
- App title
- Theme toggle button with menu (colorful, light, dark)
- Sidebar toggle button
"""

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QMenu
from PyQt6.QtCore import QSize, Qt, pyqtSignal
from PyQt6.QtGui import QFont, QAction

from core.utils import load_icon


class TopBar(QWidget):
    theme_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setObjectName("TopBar")
        self.setAcceptDrops(False)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(20)

        # Logo
        self.logo = QLabel()
        self.logo.setPixmap(load_icon("Fox.png").pixmap(36, 36))
        layout.addWidget(self.logo)

        # Title
        self.title = QLabel("FoxChat")
        self.title.setFont(QFont("Segoe UI", 28, QFont.Weight.ExtraBold))
        self.title.setObjectName("TitleLabel")
        layout.addWidget(self.title)

        layout.addStretch()

        # Theme Toggle Button
        self.btn_theme = QPushButton()
        self.btn_theme.setIcon(load_icon("Light-Dark-Mode.png"))
        self.btn_theme.setIconSize(QSize(24, 24))
        self.btn_theme.setFixedSize(44, 44)
        self.btn_theme.setObjectName("IconButton")
        self.btn_theme.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_theme.setToolTip("Change Theme")
        self.btn_theme.clicked.connect(self.show_theme_menu)
        layout.addWidget(self.btn_theme)

        # Sidebar Toggle Button
        self.btn_toggle_sidebar = QPushButton()
        self.btn_toggle_sidebar.setIcon(load_icon("Thick-Arrow-Left.png"))
        self.btn_toggle_sidebar.setIconSize(QSize(24, 24))
        self.btn_toggle_sidebar.setFixedSize(44, 44)
        self.btn_toggle_sidebar.setObjectName("IconButton")
        self.btn_toggle_sidebar.setCursor(Qt.CursorShape.PointingHandCursor)
        layout.addWidget(self.btn_toggle_sidebar)

    def show_theme_menu(self):
        menu = QMenu(self)

        colorful_action = QAction("Colorful", self)
        colorful_action.triggered.connect(lambda: self.theme_changed.emit("colorful"))
        menu.addAction(colorful_action)

        light_action = QAction("Light", self)
        light_action.triggered.connect(lambda: self.theme_changed.emit("light"))
        menu.addAction(light_action)

        dark_action = QAction("Dark", self)
        dark_action.triggered.connect(lambda: self.theme_changed.emit("dark"))
        menu.addAction(dark_action)

        menu.exec(self.btn_theme.mapToGlobal(self.btn_theme.rect().bottomLeft()))
