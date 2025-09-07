"""
Veri modelleri için temel testler
"""

import unittest
import sys
import os
from pathlib import Path

# Test için proje root'unu path'e ekle
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.models.library_models import Library, Topic, Example


class TestLibraryModels(unittest.TestCase):
    """Library model testleri"""
    
    def setUp(self):
        """Test öncesi hazırlık"""
        self.library = Library(name="Test Kütüphanesi")
        self.topic = Topic(title="Test Konusu", content="Test içeriği")
        self.example = Example(name="Test Örneği", content="print('hello')", language="python")
    
    def test_library_creation(self):
        """Kütüphane oluşturma testi"""
        self.assertEqual(self.library.name, "Test Kütüphanesi")
        self.assertEqual(len(self.library.topics), 0)
        self.assertIsNotNone(self.library.id)
    
    def test_topic_creation(self):
        """Konu oluşturma testi"""
        self.assertEqual(self.topic.title, "Test Konusu")
        self.assertEqual(self.topic.content, "Test içeriği")
        self.assertEqual(len(self.topic.children), 0)
        self.assertEqual(len(self.topic.examples), 0)
        self.assertIsNotNone(self.topic.id)
    
    def test_example_creation(self):
        """Örnek oluşturma testi"""
        self.assertEqual(self.example.name, "Test Örneği")
        self.assertEqual(self.example.content, "print('hello')")
        self.assertEqual(self.example.language, "python")
        self.assertIsNotNone(self.example.id)
    
    def test_add_topic_to_library(self):
        """Kütüphaneye konu ekleme testi"""
        self.library.add_topic(self.topic)
        self.assertEqual(len(self.library.topics), 1)
        self.assertEqual(self.library.topics[0], self.topic)
    
    def test_add_child_topic(self):
        """Alt konu ekleme testi"""
        child_topic = Topic(title="Alt Konu")
        self.topic.add_child(child_topic)
        
        self.assertEqual(len(self.topic.children), 1)
        self.assertEqual(self.topic.children[0], child_topic)
        self.assertEqual(child_topic.parent_id, self.topic.id)
    
    def test_add_example_to_topic(self):
        """Konuya örnek ekleme testi"""
        self.topic.add_example(self.example)
        self.assertEqual(len(self.topic.examples), 1)
        self.assertEqual(self.topic.examples[0], self.example)
    
    def test_find_topic_by_id(self):
        """ID ile konu bulma testi"""
        self.library.add_topic(self.topic)
        found_topic = self.library.find_topic_by_id(self.topic.id)
        self.assertEqual(found_topic, self.topic)
    
    def test_search_topics(self):
        """Konu arama testi"""
        self.topic.title = "Python Temelleri"
        self.topic.content = "Python programlama dili temelleri"
        self.library.add_topic(self.topic)
        
        # "Python" araması
        results = self.library.search_topics("Python")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], self.topic)
        
        # "Java" araması (bulunamayacak)
        results = self.library.search_topics("Java")
        self.assertEqual(len(results), 0)
    
    def test_to_dict_and_from_dict(self):
        """Dictionary dönüşümü testi"""
        # Topic'e örnek ekle
        self.topic.add_example(self.example)
        
        # Dictionary'ye çevir
        topic_dict = self.topic.to_dict()
        
        # Dictionary'den geri oluştur
        new_topic = Topic.from_dict(topic_dict)
        
        # Karşılaştır
        self.assertEqual(new_topic.title, self.topic.title)
        self.assertEqual(new_topic.content, self.topic.content)
        self.assertEqual(len(new_topic.examples), 1)
        self.assertEqual(new_topic.examples[0].name, self.example.name)


class TestDataPersistence(unittest.TestCase):
    """Veri kalıcılığı testleri"""
    
    def test_library_serialization(self):
        """Kütüphane serileştirme testi"""
        library = Library(name="Test Kütüphanesi")
        topic = Topic(title="Test Konusu")
        example = Example(name="Test Örneği", content="test", language="python")
        
        topic.add_example(example)
        library.add_topic(topic)
        
        # Dictionary'ye çevir
        library_dict = library.to_dict()
        
        # Geri oluştur
        new_library = Library.from_dict(library_dict)
        
        # Kontrol et
        self.assertEqual(new_library.name, library.name)
        self.assertEqual(len(new_library.topics), 1)
        self.assertEqual(new_library.topics[0].title, topic.title)
        self.assertEqual(len(new_library.topics[0].examples), 1)


if __name__ == '__main__':
    unittest.main()
