"""
İçerik editörü widget'ı
"""

from PySide6.QtWidgets import QTextEdit, QVBoxLayout, QWidget
from PySide6.QtCore import Signal
from PySide6.QtGui import QFont, QTextCursor, QTextCharFormat


class ContentEditor(QTextEdit):
    """Rich text içerik editörü"""
    
    # Signals
    content_changed = Signal(str)
    
    def __init__(self):
        super().__init__()
        self._setup_ui()
        self._setup_formatting()
    
    def _setup_ui(self):
        """UI ayarlarını yapar"""
        # Font ayarları
        font = QFont("Consolas", 11)
        self.setFont(font)
        
        # Editör ayarları
        self.setLineWrapMode(QTextEdit.WidgetWidth)
        self.setAcceptRichText(True)
        
        # Placeholder text
        self.setPlaceholderText("Konu içeriğinizi buraya yazabilirsiniz...\n\n"
                               "Desteklenen özellikler:\n"
                               "• **Kalın metin**\n"
                               "• *İtalik metin*\n"
                               "• [Link metni](URL)\n"
                               "• ```kod blokları```")
        
        # Signals
        self.textChanged.connect(self._on_text_changed)
    
    def _setup_formatting(self):
        """Formatting özelliklerini ayarlar"""
        # Syntax highlighting için gelecekte kullanılabilir
        pass
    
    def _on_text_changed(self):
        """Metin değiştiğinde"""
        content = self.toPlainText()
        self.content_changed.emit(content)
    
    def set_content(self, content: str):
        """İçeriği ayarlar"""
        # Markdown benzeri basit formatting uygula
        self.setPlainText(content)
    
    def get_content(self) -> str:
        """İçeriği döndürür"""
        return self.toPlainText()
    
    def toggle_bold(self):
        """Seçili metni kalın yapar/kaldırır"""
        cursor = self.textCursor()
        if cursor.hasSelection():
            selected_text = cursor.selectedText()
            
            # Basit markdown-style bold formatting
            if selected_text.startswith("**") and selected_text.endswith("**"):
                # Bold'u kaldır
                new_text = selected_text[2:-2]
            else:
                # Bold yap
                new_text = f"**{selected_text}**"
            
            cursor.insertText(new_text)
    
    def toggle_italic(self):
        """Seçili metni italik yapar/kaldırır"""
        cursor = self.textCursor()
        if cursor.hasSelection():
            selected_text = cursor.selectedText()
            
            # Basit markdown-style italic formatting
            if selected_text.startswith("*") and selected_text.endswith("*") and not selected_text.startswith("**"):
                # Italic'i kaldır
                new_text = selected_text[1:-1]
            else:
                # Italic yap
                new_text = f"*{selected_text}*"
            
            cursor.insertText(new_text)
    
    def insert_link(self):
        """Link ekler"""
        cursor = self.textCursor()
        selected_text = cursor.selectedText() if cursor.hasSelection() else "Link metni"
        
        # Markdown-style link
        link_text = f"[{selected_text}](URL_buraya)"
        cursor.insertText(link_text)
        
        # URL kısmını seç
        cursor.movePosition(QTextCursor.Left, QTextCursor.MoveAnchor, 1)
        cursor.movePosition(QTextCursor.Left, QTextCursor.KeepAnchor, 10)
        self.setTextCursor(cursor)
    
    def insert_code_block(self):
        """Kod bloku ekler"""
        cursor = self.textCursor()
        selected_text = cursor.selectedText() if cursor.hasSelection() else "kod_buraya"
        
        # Markdown-style code block
        if "\n" in selected_text:
            # Çok satırlı kod bloku
            code_text = f"```python\n{selected_text}\n```"
        else:
            # Inline kod
            code_text = f"`{selected_text}`"
        
        cursor.insertText(code_text)
    
    def insert_heading(self, level: int = 1):
        """Başlık ekler"""
        cursor = self.textCursor()
        selected_text = cursor.selectedText() if cursor.hasSelection() else "Başlık"
        
        # Markdown-style heading
        heading_prefix = "#" * level
        heading_text = f"{heading_prefix} {selected_text}"
        cursor.insertText(heading_text)
    
    def insert_list_item(self):
        """Liste öğesi ekler"""
        cursor = self.textCursor()
        cursor.insertText("• Öğe")
    
    def clear_formatting(self):
        """Formatting'i temizler"""
        self.setPlainText(self.toPlainText())
