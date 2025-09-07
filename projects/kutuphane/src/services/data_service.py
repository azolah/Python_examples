"""
JSON tabanlı veri yönetim servisi
"""

import json
import os
from typing import Optional
from pathlib import Path

from ..models.library_models import Library, Topic, Example


class DataService:
    """JSON dosyası ile veri yönetimi yapan servis"""
    
    def __init__(self, data_file_path: str = None):
        """
        DataService constructor
        
        Args:
            data_file_path: JSON dosyasının yolu. Belirtilmezse varsayılan yol kullanılır.
        """
        if data_file_path is None:
            # Proje kök dizinini bul
            current_dir = Path(__file__).parent.parent.parent
            self.data_file_path = current_dir / "data" / "library.json"
        else:
            self.data_file_path = Path(data_file_path)
        
        # Veri klasörünü oluştur
        self.data_file_path.parent.mkdir(parents=True, exist_ok=True)
        
        self._library: Optional[Library] = None
    
    def load_library(self) -> Library:
        """
        Kütüphane verisini yükler. Dosya yoksa yeni kütüphane oluşturur.
        
        Returns:
            Library: Yüklenen veya yeni oluşturulan kütüphane
        """
        if self._library is not None:
            return self._library
        
        try:
            if self.data_file_path.exists():
                with open(self.data_file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    self._library = Library.from_dict(data)
            else:
                # Varsayılan kütüphane oluştur
                self._library = self._create_default_library()
                self.save_library()
        except (json.JSONDecodeError, KeyError, Exception) as e:
            print(f"Veri yüklenirken hata oluştu: {e}")
            # Hatalı dosya varsa backup oluştur
            if self.data_file_path.exists():
                backup_path = self.data_file_path.with_suffix('.json.backup')
                self.data_file_path.rename(backup_path)
                print(f"Hatalı dosya {backup_path} olarak yedeklendi")
            
            # Yeni kütüphane oluştur
            self._library = self._create_default_library()
            self.save_library()
        
        return self._library
    
    def save_library(self) -> bool:
        """
        Kütüphane verisini kaydeder.
        
        Returns:
            bool: Kaydetme işlemi başarılı ise True
        """
        if self._library is None:
            return False
        
        try:
            # Backup oluştur
            if self.data_file_path.exists():
                backup_path = self.data_file_path.with_suffix('.json.bak')
                with open(self.data_file_path, 'r', encoding='utf-8') as original:
                    with open(backup_path, 'w', encoding='utf-8') as backup:
                        backup.write(original.read())
            
            # Yeni veriyi kaydet
            with open(self.data_file_path, 'w', encoding='utf-8') as file:
                json.dump(self._library.to_dict(), file, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"Veri kaydedilirken hata oluştu: {e}")
            return False
    
    def get_library(self) -> Library:
        """
        Mevcut kütüphaneyi döndürür. Yüklenmemişse yükler.
        
        Returns:
            Library: Kütüphane instance'ı
        """
        if self._library is None:
            return self.load_library()
        return self._library
    
    def create_backup(self, backup_path: str = None) -> bool:
        """
        Manuel backup oluşturur.
        
        Args:
            backup_path: Backup dosyasının yolu. Belirtilmezse otomatik isim verilir.
            
        Returns:
            bool: Backup oluşturma başarılı ise True
        """
        if backup_path is None:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = self.data_file_path.with_name(f"library_backup_{timestamp}.json")
        
        try:
            if self.data_file_path.exists():
                with open(self.data_file_path, 'r', encoding='utf-8') as original:
                    with open(backup_path, 'w', encoding='utf-8') as backup:
                        backup.write(original.read())
                return True
        except Exception as e:
            print(f"Backup oluşturulurken hata oluştu: {e}")
        
        return False
    
    def import_from_file(self, import_path: str) -> bool:
        """
        Başka bir JSON dosyasından veri içe aktarır.
        
        Args:
            import_path: İçe aktarılacak JSON dosyasının yolu
            
        Returns:
            bool: İçe aktarma başarılı ise True
        """
        try:
            with open(import_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                self._library = Library.from_dict(data)
                return self.save_library()
        except Exception as e:
            print(f"Veri içe aktarılırken hata oluştu: {e}")
            return False
    
    def export_to_file(self, export_path: str) -> bool:
        """
        Mevcut veriyi başka bir JSON dosyasına dışa aktarır.
        
        Args:
            export_path: Dışa aktarılacak JSON dosyasının yolu
            
        Returns:
            bool: Dışa aktarma başarılı ise True
        """
        if self._library is None:
            return False
        
        try:
            with open(export_path, 'w', encoding='utf-8') as file:
                json.dump(self._library.to_dict(), file, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Veri dışa aktarılırken hata oluştu: {e}")
            return False
    
    def _create_default_library(self) -> Library:
        """
        Varsayılan kütüphane yapısını oluşturur.
        
        Returns:
            Library: Örnek verilerle dolu varsayılan kütüphane
        """
        library = Library(
            name="Kişisel Kütüphanem",
            description="Öğrendiğim konuları organize ettiğim kişisel bilgi bankam"
        )
        
        # Örnek programlama konusu
        programming = Topic(
            title="Programlama",
            content="Programlama dilleri ve kavramlarıyla ilgili notlarım"
        )
        
        # Python alt konusu
        python = Topic(
            title="Python",
            content="Python programlama diliyle ilgili öğrendiklerim"
        )
        
        # Python temeller
        basics = Topic(
            title="Temeller",
            content="Python dilinin temel kavramları ve syntax'ı"
        )
        
        # Veri tipleri
        data_types = Topic(
            title="Veri Tipleri",
            content="""Python'da temel veri tipleri:

## Sayısal Tipler
- **int**: Tam sayılar (örn: 42, -17)
- **float**: Ondalık sayılar (örn: 3.14, -2.5)
- **complex**: Karmaşık sayılar (örn: 3+4j)

## Metin
- **str**: String/metin veriler (örn: "Merhaba Dünya")

## Boolean
- **bool**: True/False değerleri

## Koleksiyonlar
- **list**: Sıralı, değiştirilebilir koleksiyon
- **tuple**: Sıralı, değiştirilemez koleksiyon  
- **dict**: Anahtar-değer çiftleri
- **set**: Tekrar etmeyen öğeler"""
        )
        
        # Örnek kodlar ekle
        int_example = Example(
            name="Tam Sayı Örnekleri",
            content="""# Tam sayı tanımlama
yaş = 25
negatif_sayı = -42
büyük_sayı = 1000000

# Matematiksel işlemler
toplam = 10 + 5    # 15
fark = 10 - 3      # 7
çarpım = 4 * 6     # 24
bölüm = 15 // 3    # 5 (tam bölme)
kalan = 17 % 5     # 2 (mod alma)
üs = 2 ** 3        # 8 (üs alma)

print(f"Yaş: {yaş}")
print(f"Toplam: {toplam}")""",
            language="python"
        )
        
        string_example = Example(
            name="String İşlemleri",
            content='''# String tanımlama
isim = "Ahmet"
soyisim = 'Yılmaz'
mesaj = """Çok satırlı
metin örneği"""

# String birleştirme
tam_isim = isim + " " + soyisim
print(f"Tam isim: {tam_isim}")

# String metodları
büyük_harf = isim.upper()      # "AHMET"
küçük_harf = isim.lower()      # "ahmet"
uzunluk = len(isim)            # 5

# String formatting
yaş = 25
bilgi = f"İsim: {isim}, Yaş: {yaş}"
print(bilgi)''',
            language="python"
        )
        
        data_types.add_example(int_example)
        data_types.add_example(string_example)
        
        # Kontrol yapıları
        control_structures = Topic(
            title="Kontrol Yapıları",
            content="Python'da karar verme ve tekrar yapıları"
        )
        
        if_example = Example(
            name="If-Else Örneği",
            content="""# Basit if-else
yaş = 18

if yaş >= 18:
    print("Reşitsiniz")
else:
    print("Reşit değilsiniz")

# Çoklu koşul
not_değeri = 85

if not_değeri >= 90:
    harf_notu = "AA"
elif not_değeri >= 80:
    harf_notu = "BA"
elif not_değeri >= 70:
    harf_notu = "BB"
elif not_değeri >= 60:
    harf_notu = "CB"
else:
    harf_notu = "FF"

print(f"Harf notunuz: {harf_notu}")""",
            language="python"
        )
        
        control_structures.add_example(if_example)
        
        # Hiyerarşiyi oluştur
        basics.add_child(data_types)
        basics.add_child(control_structures)
        python.add_child(basics)
        programming.add_child(python)
        library.add_topic(programming)
        
        return library
