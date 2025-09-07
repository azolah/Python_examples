"""
Kişisel Kütüphane Uygulaması - Kurulum Scripti
Bu script uygulamanın gerekli bağımlılıklarını yükler ve ilk kurulumu yapar.
"""

import subprocess
import sys
import os
from pathlib import Path


def run_command(command, description=""):
    """Komut çalıştırır ve sonucu döndürür"""
    print(f"🔄 {description}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ Başarılı: {description}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Hata: {description}")
        print(f"   Detay: {e.stderr}")
        return False


def check_python_version():
    """Python sürümünü kontrol eder"""
    print("🐍 Python sürümü kontrol ediliyor...")
    if sys.version_info < (3, 8):
        print(f"❌ Python 3.8 veya daha yeni bir sürüm gerekli. Mevcut: {sys.version}")
        return False
    else:
        print(f"✅ Python sürümü uygun: {sys.version}")
        return True


def install_requirements():
    """Requirements.txt'deki paketleri yükler"""
    requirements_file = Path(__file__).parent / "requirements.txt"
    
    if not requirements_file.exists():
        print("❌ requirements.txt dosyası bulunamadı!")
        return False
    
    print("📦 Bağımlılıklar yükleniyor...")
    return run_command(
        f"{sys.executable} -m pip install -r {requirements_file}",
        "Bağımlılık kurulumu"
    )


def create_data_directory():
    """Veri klasörünü oluşturur"""
    data_dir = Path(__file__).parent / "data"
    
    if not data_dir.exists():
        print("📁 Veri klasörü oluşturuluyor...")
        data_dir.mkdir(parents=True, exist_ok=True)
        print("✅ Veri klasörü oluşturuldu")
    else:
        print("✅ Veri klasörü zaten mevcut")
    
    return True


def run_tests():
    """Basit testleri çalıştırır"""
    print("🧪 Testler çalıştırılıyor...")
    test_file = Path(__file__).parent / "tests" / "test_models.py"
    
    if test_file.exists():
        return run_command(
            f"{sys.executable} -m unittest tests.test_models",
            "Test çalıştırma"
        )
    else:
        print("⚠️  Test dosyası bulunamadı, testler atlanıyor")
        return True


def setup_environment():
    """Geliştirme ortamını hazırlar"""
    print("🛠️  Geliştirme ortamı hazırlanıyor...")
    
    # Virtual environment önerisi
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("💡 Öneri: Virtual environment kullanmanız önerilir")
        print("   python -m venv venv")
        print("   .\\venv\\Scripts\\activate  # Windows")
        print("   source venv/bin/activate  # Linux/Mac")
    
    return True


def main():
    """Ana kurulum fonksiyonu"""
    print("=" * 60)
    print("🎓 Kişisel Kütüphane Uygulaması - Kurulum")
    print("=" * 60)
    
    # Adımlar
    steps = [
        ("Python sürüm kontrolü", check_python_version),
        ("Ortam hazırlığı", setup_environment),
        ("Bağımlılık kurulumu", install_requirements),
        ("Veri klasörü oluşturma", create_data_directory),
        ("Test çalıştırma", run_tests),
    ]
    
    success_count = 0
    total_steps = len(steps)
    
    for step_name, step_function in steps:
        print(f"\n📋 Adım: {step_name}")
        print("-" * 40)
        
        if step_function():
            success_count += 1
        else:
            print(f"❌ Adım başarısız: {step_name}")
            print("Kurulum durduruldu.")
            return False
    
    # Sonuç
    print("\n" + "=" * 60)
    if success_count == total_steps:
        print("🎉 Kurulum başarıyla tamamlandı!")
        print("\n📚 Uygulama kullanıma hazır:")
        print("   python main.py")
        print("\n📖 Kullanım kılavuzu:")
        print("   - Sol panelden konular oluşturabilirsiniz")
        print("   - Orta panelde içerik yazabilirsiniz")
        print("   - Sağ panelde örnekler ekleyebilirsiniz")
        print("   - Ctrl+S ile kaydetmeyi unutmayın!")
        
        return True
    else:
        print(f"⚠️  Kurulum kısmen başarılı: {success_count}/{total_steps}")
        print("Bazı adımlar başarısız oldu. Lütfen hataları kontrol edin.")
        return False


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⚠️  Kurulum kullanıcı tarafından iptal edildi.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Beklenmeyen hata: {e}")
        sys.exit(1)
