"""
Ana uygulama ViewModel'ı
MVVM mimarisinin ViewModel katmanı - UI ile Model arasındaki köprü
"""

from typing import List, Optional, Dict, Any
from PySide6.QtCore import QObject, Signal, Property, QModelIndex
from PySide6.QtGui import QStandardItemModel, QStandardItem

from ..models.library_models import Library, Topic, Example
from ..services.data_service import DataService


class LibraryViewModel(QObject):
    """
    Kütüphane uygulamasının ana ViewModel'ı
    UI ile veri katmanı arasındaki iş mantığını yönetir
    """
    
    # Signals - UI'ın dinleyebileceği olaylar
    library_loaded = Signal()
    library_saved = Signal(bool)  # bool: başarı durumu
    topic_selected = Signal(str)  # topic_id
    example_selected = Signal(str)  # example_id
    data_changed = Signal()
    error_occurred = Signal(str)  # error_message
    
    def __init__(self, data_service: DataService = None):
        super().__init__()
        
        # Veri servisi
        self._data_service = data_service or DataService()
        
        # Mevcut durumlar
        self._current_library: Optional[Library] = None
        self._current_topic: Optional[Topic] = None
        self._current_example: Optional[Example] = None
        self._search_results: List[Topic] = []
        
        # Tree model for QTreeView
        self._tree_model: Optional[QStandardItemModel] = None
        
    # Properties - UI'ın erişebileceği özellikler
    @Property(bool, notify=library_loaded)
    def is_library_loaded(self) -> bool:
        """Kütüphane yüklenmiş mi kontrolü"""
        return self._current_library is not None
    
    @Property(str, notify=topic_selected)
    def current_topic_title(self) -> str:
        """Seçili konunun başlığı"""
        return self._current_topic.title if self._current_topic else ""
    
    @Property(str, notify=topic_selected)
    def current_topic_content(self) -> str:
        """Seçili konunun içeriği"""
        return self._current_topic.content if self._current_topic else ""
    
    @Property(str, notify=example_selected)
    def current_example_name(self) -> str:
        """Seçili örneğin adı"""
        return self._current_example.name if self._current_example else ""
    
    @Property(str, notify=example_selected)
    def current_example_content(self) -> str:
        """Seçili örneğin içeriği"""
        return self._current_example.content if self._current_example else ""
    
    @Property(str, notify=example_selected)
    def current_example_language(self) -> str:
        """Seçili örneğin programlama dili"""
        return self._current_example.language if self._current_example else "text"
    
    # Public Methods - UI'ın çağırabileceği metotlar
    def load_library(self) -> None:
        """Kütüphane verilerini yükler"""
        try:
            self._current_library = self._data_service.load_library()
            self._update_tree_model()
            self.library_loaded.emit()
        except Exception as e:
            self.error_occurred.emit(f"Kütüphane yüklenirken hata oluştu: {str(e)}")
    
    def save_library(self) -> None:
        """Kütüphane verilerini kaydeder"""
        try:
            success = self._data_service.save_library()
            self.library_saved.emit(success)
            if not success:
                self.error_occurred.emit("Veri kaydedilemedi!")
        except Exception as e:
            self.error_occurred.emit(f"Veri kaydedilirken hata oluştu: {str(e)}")
            self.library_saved.emit(False)
    
    def get_tree_model(self) -> QStandardItemModel:
        """Tree view için model döndürür"""
        if self._tree_model is None:
            self._tree_model = QStandardItemModel()
            self._tree_model.setHorizontalHeaderLabels(["Konular"])
            if self._current_library:
                self._update_tree_model()
        return self._tree_model
    
    def select_topic_by_id(self, topic_id: str) -> None:
        """ID'ye göre konu seçer"""
        if not self._current_library:
            return
        
        topic = self._current_library.find_topic_by_id(topic_id)
        if topic:
            self._current_topic = topic
            self._current_example = None  # Örnek seçimini temizle
            self.topic_selected.emit(topic_id)
    
    def select_example_by_id(self, example_id: str) -> None:
        """ID'ye göre örnek seçer"""
        if not self._current_topic:
            return
        
        for example in self._current_topic.examples:
            if example.id == example_id:
                self._current_example = example
                self.example_selected.emit(example_id)
                break
    
    def add_new_topic(self, title: str, parent_id: str = None) -> str:
        """Yeni konu ekler"""
        if not self._current_library:
            return ""
        
        new_topic = Topic(title=title)
        
        if parent_id:
            # Alt konu olarak ekle
            parent_topic = self._current_library.find_topic_by_id(parent_id)
            if parent_topic:
                parent_topic.add_child(new_topic)
        else:
            # Ana konu olarak ekle
            self._current_library.add_topic(new_topic)
        
        self._update_tree_model()
        self.data_changed.emit()
        return new_topic.id
    
    def update_topic_content(self, topic_id: str, content: str) -> None:
        """Konu içeriğini günceller"""
        if not self._current_library:
            return
        
        topic = self._current_library.find_topic_by_id(topic_id)
        if topic:
            topic.content = content
            from datetime import datetime
            topic.updated_at = datetime.now()
            self.data_changed.emit()
    
    def update_topic_title(self, topic_id: str, title: str) -> None:
        """Konu başlığını günceller"""
        if not self._current_library:
            return
        
        topic = self._current_library.find_topic_by_id(topic_id)
        if topic:
            topic.title = title
            from datetime import datetime
            topic.updated_at = datetime.now()
            self._update_tree_model()
            self.data_changed.emit()
    
    def delete_topic(self, topic_id: str) -> bool:
        """Konu siler"""
        if not self._current_library:
            return False
        
        # Ana konularda ara
        if self._current_library.remove_topic(topic_id):
            self._update_tree_model()
            self.data_changed.emit()
            return True
        
        # Alt konularda ara (recursive)
        def remove_from_children(topics: List[Topic]) -> bool:
            for topic in topics:
                if topic.remove_child(topic_id):
                    return True
                if remove_from_children(topic.children):
                    return True
            return False
        
        if remove_from_children(self._current_library.topics):
            self._update_tree_model()
            self.data_changed.emit()
            return True
        
        return False
    
    def add_new_example(self, name: str, content: str, language: str = "text") -> str:
        """Seçili konuya yeni örnek ekler"""
        if not self._current_topic:
            return ""
        
        new_example = Example(name=name, content=content, language=language)
        self._current_topic.add_example(new_example)
        self.data_changed.emit()
        return new_example.id
    
    def update_example(self, example_id: str, name: str = None, 
                      content: str = None, language: str = None) -> None:
        """Örnek günceller"""
        if not self._current_topic:
            return
        
        for example in self._current_topic.examples:
            if example.id == example_id:
                if name is not None:
                    example.name = name
                if content is not None:
                    example.content = content
                if language is not None:
                    example.language = language
                
                from datetime import datetime
                example.updated_at = datetime.now()
                self.data_changed.emit()
                break
    
    def delete_example(self, example_id: str) -> bool:
        """Örnek siler"""
        if not self._current_topic:
            return False
        
        if self._current_topic.remove_example(example_id):
            if self._current_example and self._current_example.id == example_id:
                self._current_example = None
            self.data_changed.emit()
            return True
        return False
    
    def search_topics(self, query: str) -> List[Dict[str, Any]]:
        """Konularda arama yapar"""
        if not self._current_library or not query.strip():
            return []
        
        results = self._current_library.search_topics(query)
        self._search_results = results
        
        # UI için uygun format
        return [
            {
                'id': topic.id,
                'title': topic.title,
                'content_preview': topic.content[:100] + "..." if len(topic.content) > 100 else topic.content,
                'tags': topic.tags
            }
            for topic in results
        ]
    
    def get_topic_hierarchy(self, topic_id: str) -> List[Dict[str, str]]:
        """Konunun hiyerarşisini döndürür (breadcrumb için)"""
        if not self._current_library:
            return []
        
        def find_path(topics: List[Topic], target_id: str, path: List[Topic] = None) -> Optional[List[Topic]]:
            if path is None:
                path = []
            
            for topic in topics:
                current_path = path + [topic]
                if topic.id == target_id:
                    return current_path
                
                result = find_path(topic.children, target_id, current_path)
                if result:
                    return result
            
            return None
        
        path = find_path(self._current_library.topics, topic_id)
        if path:
            return [{'id': topic.id, 'title': topic.title} for topic in path]
        return []
    
    def get_current_topic_examples(self) -> List[Dict[str, Any]]:
        """Seçili konunun örneklerini döndürür"""
        if not self._current_topic:
            return []
        
        return [
            {
                'id': example.id,
                'name': example.name,
                'language': example.language,
                'content_preview': example.content[:50] + "..." if len(example.content) > 50 else example.content
            }
            for example in self._current_topic.examples
        ]
    
    # Private Methods
    def _update_tree_model(self) -> None:
        """Tree model'ı günceller"""
        if not self._tree_model or not self._current_library:
            return
        
        self._tree_model.clear()
        self._tree_model.setHorizontalHeaderLabels(["Konular"])
        
        def add_topic_to_model(topic: Topic, parent_item: QStandardItem = None):
            item = QStandardItem(topic.title)
            item.setData(topic.id, role=256)  # Custom role for topic ID
            item.setEditable(False)
            
            if parent_item:
                parent_item.appendRow(item)
            else:
                self._tree_model.appendRow(item)
            
            # Alt konuları ekle
            for child in topic.children:
                add_topic_to_model(child, item)
        
        # Ana konuları ekle
        for topic in self._current_library.topics:
            add_topic_to_model(topic)
    
    def create_backup(self) -> bool:
        """Manuel backup oluşturur"""
        try:
            return self._data_service.create_backup()
        except Exception as e:
            self.error_occurred.emit(f"Backup oluşturulurken hata: {str(e)}")
            return False
    
    def export_data(self, file_path: str) -> bool:
        """Veriyi dışa aktarır"""
        try:
            return self._data_service.export_to_file(file_path)
        except Exception as e:
            self.error_occurred.emit(f"Dışa aktarım hatası: {str(e)}")
            return False
    
    def import_data(self, file_path: str) -> bool:
        """Veriyi içe aktarır"""
        try:
            success = self._data_service.import_from_file(file_path)
            if success:
                self._current_library = self._data_service.get_library()
                self._update_tree_model()
                self.library_loaded.emit()
            return success
        except Exception as e:
            self.error_occurred.emit(f"İçe aktarım hatası: {str(e)}")
            return False
