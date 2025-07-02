import os
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QListWidgetItem,
    QFileDialog, QMenu, QMessageBox, QApplication
)
from PyQt6.QtGui import QAction, QKeySequence, QShortcut
from PyQt6.QtCore import Qt, QTimer

from ui.components.topbar import TopBar
from ui.components.sidebar import Sidebar
from ui.input_panel import InputPanel
from ui.chat_area import ChatArea
from advanced.file_preview_widget import is_image_file

from core.utils import load_icon
from core.file_manager import (
    save_sessions, load_sessions,
    save_api_profiles, load_api_profiles
)
from core.api_manager import query_api
from core.custom_api_dialog import CustomApiDialog
from core.config import load_theme

DEFAULT_APIS = ["deepseek"]

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FoxChat")
        self.resize(1280, 850)

        self.setup_ui()
        self.setup_connections()
        self.setup_state()
        self.setAcceptDrops(True)

        self.load_sessions_for_mode()
        self.load_api_list()

    # ------------------- UI Setup ------------------- #
    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        self.topbar = TopBar()
        main_layout.addWidget(self.topbar)

        content_layout = QHBoxLayout()
        main_layout.addLayout(content_layout)

        self.sidebar = Sidebar()
        content_layout.addWidget(self.sidebar)

        self.chat_area = ChatArea()
        content_layout.addWidget(self.chat_area, 1)

        self.input_panel = InputPanel()
        main_layout.addWidget(self.input_panel)

    # ------------------- Signal/Slot Wiring ------------------- #
    def setup_connections(self):
        self.topbar.btn_toggle_sidebar.clicked.connect(self.toggle_sidebar)
        self.topbar.theme_changed.connect(self.change_theme)
        self.sidebar.btn_new_session.clicked.connect(self.create_new_session)
        self.sidebar.chat_mode_switch.currentTextChanged.connect(self.switch_chat_mode)
        self.sidebar.session_list.currentItemChanged.connect(self.switch_session)
        self.sidebar.session_list.itemChanged.connect(self.rename_session)
        self.sidebar.btn_add_api.clicked.connect(self.add_custom_api)
        self.input_panel.btn_send.clicked.connect(self.send_message)
        self.input_panel.text_input.send_requested.connect(self.send_message)
        self.input_panel.btn_upload.clicked.connect(self.open_file_dialog)

        QShortcut(QKeySequence("Ctrl+N"), self, activated=self.create_new_session)
        QShortcut(QKeySequence("Ctrl+B"), self, activated=self.toggle_sidebar)

        self.sidebar.api_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.sidebar.api_list.customContextMenuRequested.connect(self.handle_api_context_menu)
        self.sidebar.session_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.sidebar.session_list.customContextMenuRequested.connect(self.handle_session_context_menu)

    # ------------------- App State ------------------- #
    def setup_state(self):
        self.sidebar_expanded = True
        self.chat_mode = "AI Chat"
        self.ai_sessions = {}
        self.p2p_sessions = {}
        self.current_session = None
        self.waiting_for_reply = False
        self.api_profiles = DEFAULT_APIS + load_api_profiles()

    def get_current_sessions(self):
        """Helper method to get the current sessions dictionary based on chat mode."""
        return self.ai_sessions if self.chat_mode == "AI Chat" else self.p2p_sessions

    def get_current_ai_name(self):
        """Helper method to get the name of the currently selected AI."""
        ai_name = "AI"
        current_api_item = self.sidebar.api_list.currentItem()
        if current_api_item:
            ai_name = current_api_item.text()
        return ai_name

    # ------------------- Chat Logic ------------------- #
    def switch_chat_mode(self, mode):
        self.chat_mode = mode
        self.load_sessions_for_mode()
        self.chat_area.add_message(f"Switched to {mode} mode", is_user=False)
        self.sidebar.api_list.setEnabled(mode == "AI Chat")

    def create_new_session(self):
        target_sessions = self.get_current_sessions()
        count = len(target_sessions) + 1

        if self.chat_mode == "AI Chat":
            ai_name = self.get_current_ai_name()
            session_name = f"{ai_name} Chat {count}"
        else:
            session_name = f"Anonymous Chat {count}"

        target_sessions[session_name] = []

        item = QListWidgetItem(session_name)
        item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
        self.sidebar.session_list.addItem(item)
        self.sidebar.session_list.setCurrentItem(item)
        self.current_session = session_name
        self.chat_area.clear_messages()

    def rename_session(self, item):
        if item:
            new_name = item.text().strip()
            sessions = self.get_current_sessions()

            if self.current_session not in sessions:
                return  # Safety check

            if new_name in sessions and new_name != self.current_session:
                QMessageBox.warning(self, "Duplicate Name", f"A session named '{new_name}' already exists.")
                # Reset item text to previous
                item.setText(self.current_session)
                return

            # Rename session key
            sessions[new_name] = sessions.pop(self.current_session)
            self.current_session = new_name
            save_sessions(self.chat_mode, sessions)  # Save immediately

    def switch_session(self, current, _previous):
        if current is None:
            self.current_session = None
            self.chat_area.clear_messages()
            return

        new_session_name = current.text()
        sessions = self.get_current_sessions()

        if new_session_name not in sessions:
            self.current_session = None
            self.chat_area.clear_messages()
            return

        self.current_session = new_session_name
        self.load_session_messages()

    def load_sessions_for_mode(self):
        sessions = load_sessions(self.chat_mode)
        if self.chat_mode == "AI Chat":
            self.ai_sessions = sessions
        else:
            self.p2p_sessions = sessions

        self.sidebar.session_list.clear()
        for name in sessions:
            item = QListWidgetItem(name)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
            self.sidebar.session_list.addItem(item)

        if self.sidebar.session_list.count() > 0:
            self.sidebar.session_list.setCurrentRow(0)
        else:
            self.current_session = None
            self.chat_area.clear_messages()

    def load_session_messages(self):
        self.chat_area.clear_messages()
        sessions = self.get_current_sessions()
        for msg, is_user, sender in sessions.get(self.current_session, []):
            self.chat_area.add_message(msg, is_user, sender=sender)

    def send_message(self):
        if not self.current_session or self.waiting_for_reply:
            return

        text = self.input_panel.text_input.toPlainText().strip()
        files = self.input_panel.get_attached_files()
        if not text and not files:
            return

        sessions = self.get_current_sessions()
        msg = text + "".join(f"\n[Uploaded File: {f}]" for f in files)
        sessions[self.current_session].append((msg, True, "You"))
        self.chat_area.add_message(msg, True, sender="You")

        self.input_panel.text_input.clear()
        self.input_panel.clear_file_previews()
        self.set_waiting_state(True)

        if self.chat_mode == "AI Chat":
            ai_name = self.get_current_ai_name()
            QTimer.singleShot(1000, lambda: self.process_ai_reply(ai_name, text))
        else:
            # For Anonymous Chat, no AI response
            self.set_waiting_state(False)
            save_sessions(self.chat_mode, sessions)  # Save immediately for P2P chat

    def process_ai_reply(self, ai_name, user_text):
        reply = query_api(user_text, ai_name)
        sessions = self.get_current_sessions()
        sessions[self.current_session].append((reply, False, ai_name))
        self.chat_area.add_message(reply, False, sender=ai_name)
        self.set_waiting_state(False)
        save_sessions(self.chat_mode, sessions)

    def set_waiting_state(self, waiting):
        self.waiting_for_reply = waiting
        self.input_panel.btn_send.setDisabled(waiting)
        self.input_panel.text_input.setDisabled(waiting)

    # ------------------- File & API Features ------------------- #
    def get_apis_dir(self):
        """Helper method to get the path to the APIs directory."""
        return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "apis"))

    def load_api_list(self):
        self.sidebar.api_list.clear()
        for name in self.api_profiles:
            item = QListWidgetItem(load_icon("chip.png"), name)
            self.sidebar.api_list.addItem(item)

    def add_custom_api(self):
        dialog = CustomApiDialog(self)
        if dialog.exec():
            data = dialog.get_data()
            name, module, code = data["name"], data["module"], data["code"]

            # Prevent duplicates and built-in overrides
            if name in self.api_profiles or module.lower() in ["openai_api", "huggingface_api"]:
                QMessageBox.warning(self, "Duplicate", f"API '{name}' already exists or reserved.")
                return

            # Get APIs directory path
            apis_dir = self.get_apis_dir()
            os.makedirs(apis_dir, exist_ok=True)
            path = os.path.join(apis_dir, f"{module}.py")

            try:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(code)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to write API file:\n{e}")
                return

            self.api_profiles.append(name)
            # Save only custom profiles (exclude DEFAULT_APIS)
            save_api_profiles(self.api_profiles[len(DEFAULT_APIS):])
            self.load_api_list()

    def handle_api_context_menu(self, pos):
        item = self.sidebar.api_list.itemAt(pos)
        if item and item.text() not in DEFAULT_APIS:
            menu = QMenu(self)
            action = QAction(load_icon("Delete.png"), "Delete API", self)
            action.triggered.connect(lambda: self.delete_api(item.text()))
            menu.addAction(action)
            menu.exec(self.sidebar.api_list.viewport().mapToGlobal(pos))

    def delete_api(self, name):
        if name not in self.api_profiles:
            return

        self.api_profiles.remove(name)
        save_api_profiles(self.api_profiles[len(DEFAULT_APIS):])
        self.load_api_list()

        # Get APIs directory path
        apis_dir = self.get_apis_dir()
        # Try to find the module file - could be named after the module or derived from the API name
        possible_filenames = [
            f"{name.lower().replace(' ', '_')}.py",  # Based on API name
            f"{name.lower().replace(' ', '_')}_api.py"  # Based on API name with _api suffix
        ]

        for filename in possible_filenames:
            module_file = os.path.join(apis_dir, filename)
            if os.path.exists(module_file):
                try:
                    os.remove(module_file)
                    break  # Exit loop after successful deletion
                except Exception as e:
                    QMessageBox.warning(self, "Warning", f"Failed to delete API file {filename}:\n{e}")

    def handle_session_context_menu(self, pos):
        item = self.sidebar.session_list.itemAt(pos)
        if item:
            menu = QMenu(self)
            action = QAction(load_icon("Delete.png"), "Delete Chat", self)
            action.triggered.connect(lambda: self.delete_chat(item.text()))
            menu.addAction(action)
            menu.exec(self.sidebar.session_list.viewport().mapToGlobal(pos))

    def delete_chat(self, name):
        sessions = self.get_current_sessions()
        if name in sessions:
            del sessions[name]
            save_sessions(self.chat_mode, sessions)
            self.load_sessions_for_mode()

    def open_file_dialog(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        if dialog.exec():
            for f in dialog.selectedFiles():
                self.input_panel.add_file_preview(f)

    # ---------- Drag & Drop ----------

    def dragEnterEvent(self, event):
        """
        Accept drag event if it contains URLs (files) or text.
        """
        if event.mimeData().hasUrls() or event.mimeData().hasText():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        """
        Handle dropped files or text.
        Adds files to input_panel file previews,
        or inserts dropped text into the text input.
        """
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                file_path = url.toLocalFile()
                if os.path.isfile(file_path):
                    self.input_panel.add_file_preview(file_path)
            event.acceptProposedAction()
        elif event.mimeData().hasText():
            self.input_panel.text_input.insertPlainText(event.mimeData().text())
            event.acceptProposedAction()
        else:
            event.ignore()

    # ------------------- Sidebar toggle ------------------- #
    def toggle_sidebar(self):
        if self.sidebar_expanded:
            self.sidebar.hide()
            self.sidebar_expanded = False
            self.topbar.btn_toggle_sidebar.setIcon(load_icon("Thick-Arrow-Right.png"))
        else:
            self.sidebar.show()
            self.sidebar_expanded = True
            self.topbar.btn_toggle_sidebar.setIcon(load_icon("Thick-Arrow-Left.png"))

    # ------------------- Theme switching ------------------- #
    def change_theme(self, theme_name):
        """
        Change the application theme.

        Args:
            theme_name (str): Name of the theme to apply ("colorful", "light", or "dark")
        """
        load_theme(QApplication.instance(), mode=theme_name)
        print(f"Theme changed to: {theme_name}")
