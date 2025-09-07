"""
Kişisel Kütüphane Uygulaması
Ana giriş noktası

Bu uygulama öğrenilen bilgileri hiyerarşik bir yapıda organize etmek
ve görüntülemek için geliştirilmiş masaüstü uygulamasıdır.

Kullanım:
    python main.py

Mimari:
    - MVVM (Model-View-ViewModel) mimarisi
    - PySide6 (Qt for Python) UI framework
    - JSON tabanlı veri saklama
    - Modüler yapı
"""

import sys
import os
from pathlib import Path

# Proje kök dizinini Python path'ine ekle
project_root = Path(__file__).parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# PySide6 import'u
try:
    from PySide6.QtWidgets import QApplication, QMessageBox
    from PySide6.QtCore import Qt
    from PySide6.QtGui import QIcon
except ImportError as e:
    print("HATA: PySide6 kütüphanesi bulunamadı!")
    print("Lütfen aşağıdaki komutu çalıştırarak PySide6'yı yükleyin:")
    print("pip install PySide6")
    print(f"Detay: {e}")
    sys.exit(1)

# Uygulama modülleri
try:
    from src.views.main_window import MainWindow
    from src.services.data_service import DataService
except ImportError as e:
    print(f"HATA: Uygulama modülleri yüklenemedi: {e}")
    print("Lütfen proje yapısının doğru olduğundan emin olun.")
    sys.exit(1)


class LibraryApplication:
    """Ana uygulama sınıfı"""
    
    def __init__(self):
        """Uygulama başlatıcısı"""
        self.app = None
        self.main_window = None
    
    def setup_application(self):
        """Qt uygulamasını yapılandırır"""
        # QApplication oluştur
        self.app = QApplication(sys.argv)
        
        # Uygulama bilgileri
        self.app.setApplicationName("Kişisel Kütüphane")
        self.app.setApplicationVersion("1.0.0")
        self.app.setOrganizationName("KişiselKütüphane")
        self.app.setOrganizationDomain("kisiselkutuphane.local")
        
        # Windows'ta high DPI desteği
        if hasattr(Qt, 'AA_EnableHighDpiScaling'):
            self.app.setAttribute(Qt.AA_EnableHighDpiScaling, True)
        if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
            self.app.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
        
        # Uygulama ikonunu ayarla (opsiyonel)
        # icon_path = project_root / "assets" / "icons" / "app_icon.png"
        # if icon_path.exists():
        #     self.app.setWindowIcon(QIcon(str(icon_path)))
    
    def create_main_window(self):
        """Ana pencereyi oluşturur"""
        try:
            self.main_window = MainWindow()
            return True
        except Exception as e:
            self.show_error_dialog(
                "Uygulama Başlatma Hatası",
                f"Ana pencere oluşturulurken hata oluştu:\n{str(e)}"
            )
            return False
    
    def show_error_dialog(self, title: str, message: str):
        """Hata diyalogu gösterir"""
        if self.app:
            QMessageBox.critical(None, title, message)
        else:
            print(f"HATA - {title}: {message}")
    
    def run(self):
        """Uygulamayı çalıştırır"""
        try:
            # Qt uygulamasını ayarla
            self.setup_application()
            
            # Ana pencereyi oluştur
            if not self.create_main_window():
                return 1
            
            # Pencereyi göster
            self.main_window.show()
            
            # Başlangıç mesajı
            print("🚀 Kişisel Kütüphane Uygulaması başlatıldı!")
            print("📚 Öğrendiğiniz bilgileri organize etmeye başlayabilirsiniz.")
            
            # Ana event loop'u başlat
            return self.app.exec()
            
        except KeyboardInterrupt:
            print("\n⚠️  Uygulama kullanıcı tarafından durduruldu.")
            return 0
        except Exception as e:
            self.show_error_dialog(
                "Kritik Hata",
                f"Uygulama çalıştırılırken kritik bir hata oluştu:\n{str(e)}"
            )
            return 1
        finally:
            # Temizlik işlemleri
            if self.main_window:
                try:
                    # Son değişiklikleri kaydet
                    self.main_window.view_model.save_library()
                except:
                    pass
            print("👋 Uygulama kapatıldı.")


def check_dependencies():
    """Gerekli bağımlılıkların kontrol edilmesi"""
    missing_deps = []
    
    # PySide6 kontrolü
    try:
        import PySide6
    except ImportError:
        missing_deps.append("PySide6")
    
    # Pygments kontrolü (opsiyonel)
    try:
        import pygments
    except ImportError:
        print("⚠️  Pygments kütüphanesi bulunamadı. Syntax highlighting devre dışı.")
    
    # Markdown kontrolü (opsiyonel)
    try:
        import markdown
    except ImportError:
        print("⚠️  Markdown kütüphanesi bulunamadı. Markdown desteği sınırlı.")
    
    if missing_deps:
        print("❌ Eksik bağımlılıklar:")
        for dep in missing_deps:
            print(f"   - {dep}")
        print("\nLütfen aşağıdaki komutu çalıştırın:")
        print("pip install -r requirements.txt")
        return False
    
    return True


def main():
    """Ana fonksiyon"""
    print("=" * 50)
    print("🎓 Kişisel Kütüphane Uygulaması v1.0")
    print("📖 Bilgi Organizasyon ve Yönetim Sistemi")
    print("=" * 50)
    
    # Bağımlılık kontrolü
    if not check_dependencies():
        return 1
    
    # Proje yapısı kontrolü
    required_dirs = [
        project_root / "src",
        project_root / "data",
        project_root / "assets"
    ]
    
    for dir_path in required_dirs:
        if not dir_path.exists():
            print(f"⚠️  Gerekli klasör bulunamadı: {dir_path}")
            print("Proje yapısını kontrol edin.")
    
    # Uygulamayı başlat
    app = LibraryApplication()
    exit_code = app.run()
    
    return exit_code


if __name__ == "__main__":
    # Python sürüm kontrolü
    if sys.version_info < (3, 8):
        print("❌ Bu uygulama Python 3.8 veya daha yeni bir sürüm gerektirir.")
        print(f"Mevcut sürüm: {sys.version}")
        sys.exit(1)
    
    # Ana fonksiyonu çalıştır
    sys.exit(main())
