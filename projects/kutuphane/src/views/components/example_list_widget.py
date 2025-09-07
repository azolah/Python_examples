"""
Örnek listesi widget'ı
"""

from typing import List, Dict, Any
from PySide6.QtWidgets import QListWidget, QListWidgetItem
from PySide6.QtCore import Signal


class ExampleListWidget(QListWidget):
    """Örnekleri gösteren liste widget'ı"""
    
    # Signals
    example_selected = Signal(str)  # example_id
    
    def __init__(self):
        super().__init__()
        self._setup_ui()
        self._examples = []
    
    def _setup_ui(self):
        """UI ayarlarını yapar"""
        # Liste ayarları
        self.setAlternatingRowColors(True)
        self.setSelectionMode(QListWidget.SingleSelection)
        
        # Signals
        self.itemClicked.connect(self._on_item_clicked)
    
    def update_examples(self, examples: List[Dict[str, Any]]):
        """Örnek listesini günceller"""
        self._examples = examples
        self.clear()
        
        for example in examples:
            item = QListWidgetItem()
            item.setText(f"{example['name']}")
            item.setToolTip(f"Dil: {example['language']}\n{example['content_preview']}")
            item.setData(256, example['id'])  # Custom role for example ID
            self.addItem(item)
    
    def _on_item_clicked(self, item: QListWidgetItem):
        """Liste öğesine tıklandığında"""
        example_id = item.data(256)
        if example_id:
            self.example_selected.emit(example_id)
    
    def get_selected_example_id(self) -> str:
        """Seçili örneğin ID'sini döndürür"""
        current_item = self.currentItem()
        if current_item:
            return current_item.data(256)
        return ""
