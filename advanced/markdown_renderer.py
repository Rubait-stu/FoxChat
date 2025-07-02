import markdown
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.tables import TableExtension
from markdown.extensions.fenced_code import FencedCodeExtension
from markdown.extensions.nl2br import Nl2BrExtension
from markdown.extensions.sane_lists import SaneListExtension

from PyQt6.QtWidgets import QTextBrowser
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtCore import QUrl

def render_markdown(text: str) -> str:
    """
    Render markdown text to HTML using Python-Markdown with extensions.
    Returns HTML string suitable for PyQt rich text display.
    """
    try:
        html = markdown.markdown(
            text,
            extensions=[
                CodeHiliteExtension(noclasses=True, pygments_style='friendly'),
                FencedCodeExtension(),
                TableExtension(),
                SaneListExtension(),
                Nl2BrExtension(),
            ],
            output_format="html5",
        )
        return html
    except Exception as e:
        # Optional: return plain escaped text or empty on failure
        return f"<pre>{text}</pre>"

class MarkdownViewer(QTextBrowser):
    """
    A QTextBrowser subclass to display rendered markdown with link handling.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setOpenExternalLinks(False)  # We handle links ourselves
        self.anchorClicked.connect(self.handle_link_click)
        self.setReadOnly(True)
        self.setStyleSheet("border: none;")

    def set_markdown(self, markdown_text: str):
        """
        Render and set markdown text in the viewer.
        """
        html = render_markdown(markdown_text)
        self.setHtml(html)

    def handle_link_click(self, url: QUrl):
        """
        Open clicked links in the default system browser.
        """
        QDesktopServices.openUrl(url)
