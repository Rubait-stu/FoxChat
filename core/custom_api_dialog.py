# core/custom_api_dialog.py

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QTextEdit, QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt


class CustomApiDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Custom API")
        self.setMinimumWidth(400)

        layout = QVBoxLayout(self)

        # API Name
        layout.addWidget(QLabel("API Name:"))
        self.name_input = QLineEdit()
        layout.addWidget(self.name_input)

        # Python module filename (used for saving)
        layout.addWidget(QLabel("Module Filename (e.g., my_api):"))
        self.module_input = QLineEdit()
        layout.addWidget(self.module_input)

        # API Key environment variable (optional)
        layout.addWidget(QLabel("API Key Variable Name (in .env, optional):"))
        self.api_key_input = QLineEdit()
        layout.addWidget(self.api_key_input)

        # Query code snippet
        layout.addWidget(QLabel("Custom Query Code (must define a 'query(text)' function):"))
        self.code_input = QTextEdit()
        self.code_input.setPlaceholderText(
            "def query(text):\n    return 'Your response'"
        )
        layout.addWidget(self.code_input)

        # Buttons
        button_layout = QHBoxLayout()
        self.btn_save = QPushButton("Save")
        self.btn_cancel = QPushButton("Cancel")
        self.btn_save.clicked.connect(self.validate)
        self.btn_cancel.clicked.connect(self.reject)
        button_layout.addStretch()
        button_layout.addWidget(self.btn_cancel)
        button_layout.addWidget(self.btn_save)
        layout.addLayout(button_layout)

    def get_data(self) -> dict:
        """Return collected API info as a dictionary."""
        return {
            "name": self.name_input.text().strip(),
            "module": self.module_input.text().strip(),
            "api_key_var": self.api_key_input.text().strip(),
            "code": self.code_input.toPlainText().strip()
        }

    def validate(self):
        """Validate required fields before accepting."""
        data = self.get_data()
        if not data["name"] or not data["module"] or not data["code"]:
            QMessageBox.warning(
                self,
                "Missing Fields",
                "API Name, Module Filename, and Code are required."
            )
            return
        self.accept()

    def get_api_info(self):
        """Return API name and full data dict."""
        data = self.get_data()
        return data["name"], data
