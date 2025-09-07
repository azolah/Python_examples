"""
Konu ağacı widget'ı
"""

from PySide6.QtWidgets import QTreeView, QHeaderView
from PySide6.QtCore import Signal, QModelIndex
from PySide6.QtGui import QStandardItemModel


class TopicTreeWidget(QTreeView):
    """Konuları hiyerarşik olarak gösteren tree widget"""
    
    # Signals
    topic_selected = Signal(str)  # topic_id
    
    def __init__(self):
        super().__init__()
        self._setup_ui()
        self._selected_topic_id = None
    
    def _setup_ui(self):
        """UI ayarlarını yapar"""
        # Tree görünüm ayarları
        self.setAlternatingRowColors(True)
        self.setExpandsOnDoubleClick(True)
        self.setAnimated(True)
        
        # Header ayarları
        header = self.header()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        header.setStretchLastSection(True)
        
        # Selection ayarları
        self.setSelectionMode(QTreeView.SingleSelection)
        
        # Signals
        self.clicked.connect(self._on_item_clicked)
        self.doubleClicked.connect(self._on_item_double_clicked)
    
    def set_model(self, model: QStandardItemModel):
        """Tree model'ını ayarlar"""
        super().setModel(model)
        # İlk seviyeyi expand et
        if model.rowCount() > 0:
            for i in range(model.rowCount()):
                index = model.index(i, 0)
                self.expand(index)
    
    def _on_item_clicked(self, index: QModelIndex):
        """Tree item'a tıklandığında"""
        if index.isValid():
            item = self.model().itemFromIndex(index)
            topic_id = item.data(256)  # Custom role for topic ID
            if topic_id:
                self._selected_topic_id = topic_id
                self.topic_selected.emit(topic_id)
    
    def _on_item_double_clicked(self, index: QModelIndex):
        """Tree item'a çift tıklandığında"""
        if index.isValid():
            # Expand/collapse toggle
            if self.isExpanded(index):
                self.collapse(index)
            else:
                self.expand(index)
    
    def get_selected_topic_id(self) -> str:
        """Seçili konunun ID'sini döndürür"""
        return self._selected_topic_id
