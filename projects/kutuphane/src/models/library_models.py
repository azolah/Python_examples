"""
Kütüphane veri modellerini tanımlar.
"""

from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime
import uuid


@dataclass
class Example:
    """Örnek kod/snippet modeli"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    content: str = ""
    language: str = "text"
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """Modeli dictionary'ye çevirir"""
        return {
            'id': self.id,
            'name': self.name,
            'content': self.content,
            'language': self.language,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Example':
        """Dictionary'den model oluşturur"""
        return cls(
            id=data.get('id', str(uuid.uuid4())),
            name=data.get('name', ''),
            content=data.get('content', ''),
            language=data.get('language', 'text'),
            created_at=datetime.fromisoformat(data.get('created_at', datetime.now().isoformat())),
            updated_at=datetime.fromisoformat(data.get('updated_at', datetime.now().isoformat()))
        )


@dataclass
class Topic:
    """Konu/başlık modeli"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    title: str = ""
    content: str = ""
    parent_id: Optional[str] = None
    children: List['Topic'] = field(default_factory=list)
    examples: List[Example] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    is_expanded: bool = False

    def add_child(self, child: 'Topic') -> None:
        """Alt konu ekler"""
        child.parent_id = self.id
        self.children.append(child)
        self.updated_at = datetime.now()

    def remove_child(self, child_id: str) -> bool:
        """Alt konu siler"""
        for i, child in enumerate(self.children):
            if child.id == child_id:
                del self.children[i]
                self.updated_at = datetime.now()
                return True
        return False

    def add_example(self, example: Example) -> None:
        """Örnek ekler"""
        self.examples.append(example)
        self.updated_at = datetime.now()

    def remove_example(self, example_id: str) -> bool:
        """Örnek siler"""
        for i, example in enumerate(self.examples):
            if example.id == example_id:
                del self.examples[i]
                self.updated_at = datetime.now()
                return True
        return False

    def get_depth(self) -> int:
        """Hiyerarşideki derinliği hesaplar"""
        depth = 0
        current = self
        while current.parent_id:
            depth += 1
            # Parent'ı bulmak için root'tan traverse etmek gerekir
            # Bu metod optimize edilebilir
            break
        return depth

    def to_dict(self) -> Dict[str, Any]:
        """Modeli dictionary'ye çevirir"""
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'parent_id': self.parent_id,
            'children': [child.to_dict() for child in self.children],
            'examples': [example.to_dict() for example in self.examples],
            'tags': self.tags,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'is_expanded': self.is_expanded
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Topic':
        """Dictionary'den model oluşturur"""
        topic = cls(
            id=data.get('id', str(uuid.uuid4())),
            title=data.get('title', ''),
            content=data.get('content', ''),
            parent_id=data.get('parent_id'),
            tags=data.get('tags', []),
            created_at=datetime.fromisoformat(data.get('created_at', datetime.now().isoformat())),
            updated_at=datetime.fromisoformat(data.get('updated_at', datetime.now().isoformat())),
            is_expanded=data.get('is_expanded', False)
        )
        
        # Children'ları yükle
        for child_data in data.get('children', []):
            child = cls.from_dict(child_data)
            topic.children.append(child)
        
        # Examples'ları yükle
        for example_data in data.get('examples', []):
            example = Example.from_dict(example_data)
            topic.examples.append(example)
        
        return topic


@dataclass
class Library:
    """Kütüphane ana modeli"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = "Kişisel Kütüphanem"
    description: str = ""
    topics: List[Topic] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    version: str = "1.0.0"

    def add_topic(self, topic: Topic) -> None:
        """Ana konu ekler"""
        self.topics.append(topic)
        self.updated_at = datetime.now()

    def remove_topic(self, topic_id: str) -> bool:
        """Ana konu siler"""
        for i, topic in enumerate(self.topics):
            if topic.id == topic_id:
                del self.topics[i]
                self.updated_at = datetime.now()
                return True
        return False

    def find_topic_by_id(self, topic_id: str) -> Optional[Topic]:
        """ID'ye göre konu bulur (recursive)"""
        def search_in_topic(topic: Topic) -> Optional[Topic]:
            if topic.id == topic_id:
                return topic
            for child in topic.children:
                result = search_in_topic(child)
                if result:
                    return result
            return None

        for topic in self.topics:
            result = search_in_topic(topic)
            if result:
                return result
        return None

    def search_topics(self, query: str) -> List[Topic]:
        """Konularda arama yapar"""
        results = []
        query_lower = query.lower()

        def search_in_topic(topic: Topic):
            if (query_lower in topic.title.lower() or 
                query_lower in topic.content.lower() or
                any(query_lower in tag.lower() for tag in topic.tags)):
                results.append(topic)
            
            for child in topic.children:
                search_in_topic(child)

        for topic in self.topics:
            search_in_topic(topic)
        
        return results

    def to_dict(self) -> Dict[str, Any]:
        """Modeli dictionary'ye çevirir"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'topics': [topic.to_dict() for topic in self.topics],
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'version': self.version
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Library':
        """Dictionary'den model oluşturur"""
        library = cls(
            id=data.get('id', str(uuid.uuid4())),
            name=data.get('name', 'Kişisel Kütüphanem'),
            description=data.get('description', ''),
            created_at=datetime.fromisoformat(data.get('created_at', datetime.now().isoformat())),
            updated_at=datetime.fromisoformat(data.get('updated_at', datetime.now().isoformat())),
            version=data.get('version', '1.0.0')
        )
        
        # Topics'leri yükle
        for topic_data in data.get('topics', []):
            topic = Topic.from_dict(topic_data)
            library.topics.append(topic)
        
        return library
