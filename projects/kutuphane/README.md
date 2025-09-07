# 📚 Kişisel Kütüphane Uygulaması

## 🎯 Proje Açıklaması
Öğrenilen bilgileri hiyerarşik bir yapıda organize etmek ve görüntülemek için geliştirilmiş **profesyonel masaüstü uygulaması**. Bu proje hem pratik bir araç hem de **Python, OOP, MVVM mimarisi, GUI programlama** ve **yazılım tasarım desenlerini** öğrenmek için tasarlanmıştır.

## ✨ Özellikler
- ✅ **Hiyerarşik bilgi yapısı** (Ağaç görünümü)
- ✅ **Zengin metin editörü** (Markdown desteği)
- ✅ **Örnek kod/snippet yönetimi** (Syntax highlighting)
- ✅ **JSON tabanlı veri saklama** (Backup desteği)
- ✅ **Responsive 3-panel tasarım** (Yeniden boyutlandırılabilir)
- ✅ **Otomatik kaydetme** (30 saniye aralıklarla)
- ✅ **Arama sistemi** (İçerik ve başlık araması)
- ✅ **Dışa/İçe aktarma** (JSON formatında)
- ✅ **Kapsamlı test sistemi** (Unit testler)
- ✅ **Modern UI** (QSS stil sistemi)

## 🛠️ Teknoloji Stack
- **Frontend**: PySide6 (Qt for Python) - Profesyonel UI framework
- **Mimari**: MVVM (Model-View-ViewModel) - Temiz kod mimarisi
- **Veri**: JSON - Basit ve okunabilir veri formatı
- **Rich Text**: Markdown - Kolay formatlama
- **Syntax Highlighting**: Pygments - Kod renklendirme
- **Testing**: unittest - Python standart test framework

## 🚀 Hızlı Başlangıç

### Otomatik Kurulum
```bash
# Tek komutla kurulum ve çalıştırma
python setup.py
python main.py
```

### Manuel Kurulum
```bash
# 1. Bağımlılıkları yükle
pip install -r requirements.txt

# 2. Uygulamayı başlat
python main.py
```

### Sistem Gereksinimleri
- Python 3.8+
- Windows 10+ / macOS 10.14+ / Ubuntu 18.04+
- 100MB boş disk alanı

## 📖 Kullanım
1. **Sol Panel**: Konular ve alt konular oluşturun
2. **Orta Panel**: İçerik yazın (Markdown desteği)
3. **Sağ Panel**: Kod örnekleri ekleyin
4. **Arama**: Sol üstten konularda arama yapın
5. **Kaydetme**: Ctrl+S veya otomatik kaydetme

Detaylı kullanım için: [USAGE_GUIDE.md](USAGE_GUIDE.md)

## 🏗️ Proje Yapısı
```
kutuphane/
├── main.py                 # 🚀 Ana uygulama giriş noktası
├── requirements.txt        # 📦 Python bağımlılıkları
├── setup.py               # ⚙️ Otomatik kurulum scripti
├── src/                   # 📂 Kaynak kodlar
│   ├── models/            # 🗃️ Veri modelleri (Topic, Example, Library)
│   │   ├── __init__.py
│   │   └── library_models.py
│   ├── views/             # 🎨 UI bileşenleri (PySide6)
│   │   ├── __init__.py
│   │   ├── main_window.py
│   │   └── components/
│   │       ├── topic_tree_widget.py
│   │       ├── content_editor.py
│   │       └── example_list_widget.py
│   ├── viewmodels/        # 🧠 İş mantığı (MVVM)
│   │   ├── __init__.py
│   │   └── library_viewmodel.py
│   ├── services/          # 💾 Veri servisleri (JSON)
│   │   ├── __init__.py
│   │   └── data_service.py
│   └── utils/             # 🔧 Yardımcı fonksiyonlar
│       ├── __init__.py
│       ├── syntax_highlighter.py
│       └── markdown_processor.py
├── data/                  # 📊 Kütüphane verileri
│   └── library.json       # Ana veri dosyası
├── assets/               
│   ├── icons/             # 🎯 Uygulama ikonları
│   └── styles/            # 🎨 CSS stil dosyaları
│       └── main.qss
├── tests/                 # 🧪 Test dosyaları
│   ├── __init__.py
│   └── test_models.py
├── README.md              # 📄 Bu dosya
└── USAGE_GUIDE.md         # 📚 Detaylı kullanım kılavuzu
```

## 🏛️ MVVM Mimarisi Detayı

### **Model** (Veri Katmanı)
```python
# Pure Python veri modelleri - UI'dan bağımsız
class Library:    # 📚 Ana kütüphane modeli
class Topic:      # 📝 Konu/başlık modeli  
class Example:    # 💻 Kod örneği modeli
```

### **View** (UI Katmanı)
```python
# PySide6 UI bileşenleri - sadece görünüm
class MainWindow:          # 🏠 Ana pencere
class TopicTreeWidget:     # 🌳 Sol ağaç görünümü
class ContentEditor:       # ✏️ Orta içerik editörü
class ExampleListWidget:   # 📋 Sağ örnek listesi
```

### **ViewModel** (İş Mantığı)
```python
# UI ile Model arası köprü - iş kuralları
class LibraryViewModel:    # 🎯 Ana iş mantığı yöneticisi
```

### **Service** (Veri Yönetimi)
```python
# Veri kalıcılığı ve dış sistem entegrasyonu
class DataService:         # 💾 JSON dosya yönetimi
```

## 📚 Öğrenme Hedefleri

Bu projede şunları öğrenebilirsiniz:

### 🐍 Python Geliştirme
- **OOP Prensipleri**: Encapsulation, Inheritance, Polymorphism
- **SOLID Prensipleri**: Single Responsibility, Open/Closed, vs.
- **Design Patterns**: Observer, Strategy, Factory
- **Exception Handling**: Try/except, custom exceptions
- **File I/O Operations**: JSON reading/writing, file management
- **Testing**: unittest, mocking, test-driven development

### 🎨 GUI Programlama
- **PySide6/Qt Framework**: Widgets, Layouts, Signals/Slots
- **Event-Driven Programming**: User interactions, async operations
- **Styling**: QSS (Qt Style Sheets), theme management
- **Responsive Design**: Splitters, size policies, scaling

### 🏗️ Yazılım Mimarisi
- **MVVM Pattern**: Separation of concerns, testability
- **Modular Design**: Package structure, imports, dependencies
- **Configuration Management**: Settings, constants, environment
- **Documentation**: Docstrings, README, user guides

### 💼 Profesyonel Geliştirme
- **Version Control**: Git best practices
- **Code Quality**: Linting, formatting, conventions
- **Project Structure**: Professional layout, build systems
- **Deployment**: Packaging, distribution, setup scripts

## 🧪 Test Sistemi
```bash
# Tüm testleri çalıştır
python -m unittest tests.test_models -v

# Spesifik test sınıfı
python -m unittest tests.test_models.TestLibraryModels -v

# Tek test metodu
python -m unittest tests.test_models.TestLibraryModels.test_library_creation -v
```

**Test Kapsamı**: ✅ Model oluşturma, ✅ CRUD işlemleri, ✅ Arama, ✅ Serileştirme

## 🎯 Gelecek Geliştirmeler

### Kısa Vadeli (v1.1)
- [ ] **Etiket Sistemi**: Konuları etiketlerle kategorize etme
- [ ] **Gelişmiş Arama**: Regex, filtreler, tarih aralığı
- [ ] **Favoriler**: Sık kullanılan konuları işaretleme
- [ ] **Drag & Drop**: Konuları sürükle-bırak ile organize etme

### Orta Vadeli (v2.0)
- [ ] **SQLite Entegrasyonu**: Performans ve kompleks sorgular
- [ ] **Plugin Sistemi**: Üçüncü parti eklentiler
- [ ] **Tema Sistemi**: Dark mode, özel temalar
- [ ] **Export Options**: PDF, HTML, Word formatları

### Uzun Vadeli (v3.0)
- [ ] **Cloud Sync**: Google Drive, Dropbox entegrasyonu
- [ ] **Collaborative Features**: Team sharing, comments
- [ ] **Mobile App**: React Native companion app
- [ ] **AI Integration**: Smart categorization, content suggestions

## 🤝 Katkıda Bulunma

Bu proje eğitim amaçlı olduğu için katkılarınızı memnuniyetle karşılıyoruz!

### Nasıl Katkıda Bulunabilirsiniz?
1. **🐛 Bug Reports**: Hata bulduğunuzda issue açın
2. **💡 Feature Requests**: Yeni özellik önerilerinizi paylaşın
3. **📖 Documentation**: Dokümantasyonu geliştirin
4. **🧪 Testing**: Test coverage'ı artırın
5. **🎨 UI/UX**: Kullanıcı deneyimini iyileştirin

### Geliştirme Süreci
```bash
# 1. Fork ve clone
git clone https://github.com/username/kutuphane.git

# 2. Feature branch oluştur
git checkout -b feature/amazing-feature

# 3. Değişiklikleri yap ve test et
python -m unittest

# 4. Commit ve push
git commit -m "feat: add amazing feature"
git push origin feature/amazing-feature

# 5. Pull Request oluştur
```

### Kod Standartları
- **PEP 8**: Python kod stil kılavuzu
- **Type Hints**: Fonksiyon parametreleri ve dönüş tipleri
- **Docstrings**: Tüm public metotlar için
- **Tests**: Yeni özellikler için test yazma zorunlu

## 📞 Destek ve İletişim

### 📋 Hata Bildirimi
Hata bulduğunuzda lütfen şu bilgileri paylaşın:
- **İşletim Sistemi**: Windows 10, macOS Big Sur, vs.
- **Python Sürümü**: `python --version`
- **Hata Adımları**: Hatayı tekrar oluşturma adımları
- **Log Çıktısı**: Terminal'deki hata mesajları
- **Screenshots**: Varsa ekran görüntüleri

### 💬 İletişim Kanalları
- **GitHub Issues**: Teknik sorular ve bug raporları
- **Discussions**: Genel sorular ve öneriler
- **Email**: [your-email@domain.com]

### 📚 Ek Kaynaklar
- [PySide6 Documentation](https://doc.qt.io/qtforpython/)
- [MVVM Pattern Explained](https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93viewmodel)
- [Qt Style Sheets Reference](https://doc.qt.io/qt-6/stylesheet-reference.html)
- [Python Testing Best Practices](https://realpython.com/python-testing/)

## 📜 Lisans
Bu proje MIT lisansı altında yayınlanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

## 🙏 Teşekkürler
- **Qt/PySide6 Team**: Harika UI framework'ü için
- **Python Community**: Zengin ekosistem için  
- **Contributors**: Bu projeyi geliştiren herkese

---

**💡 İpucu**: Bu README'yi uygulamanın içinde de saklamayı unutmayın! "Proje Dokümantasyonu" konusu oluşturup içeriği ekleyin. 🚀

**🎓 Öğrenim**: Her modülde detaylı yorumlar ve açıklamalar bulunmaktadır. Kodu inceleyerek Python ve GUI programlamanın inceliklerini öğrenebilirsiniz!
