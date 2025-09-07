# 📚 Kişisel Kütüphane Uygulaması - Kullanım Kılavuzu

## 🚀 Başlangıç

### Kurulum
```bash
# 1. Bağımlılıkları yükle
pip install -r requirements.txt

# 2. Uygulamayı başlat
python main.py

# Alternatif: Kurulum scripti ile
python setup.py
```

### İlk Kullanım
1. Uygulama açıldığında boş bir kütüphane görürsünüz
2. Sol panelde "➕ Konu Ekle" butonuna tıklayın
3. İlk konunuzu oluşturun (örn: "Programlama")
4. Orta panelde içerik yazmaya başlayın!

## 🎯 Temel Özellikler

### 📖 Konu Yönetimi
- **Yeni Konu Ekleme**: Sol paneldeki "➕" butonu
- **Hiyerarşik Yapı**: Konular altında alt konular oluşturabilirsiniz
- **Konu Seçimi**: Tree'de tıklayarak konu seçin
- **Konu Düzenleme**: Seçili konuda "✏️" butonu

### ✍️ İçerik Yazma
- **Markdown Desteği**: 
  - `**kalın**` → **kalın**
  - `*italik*` → *italik*
  - `[link](URL)` → [link](URL)
  - `` `kod` `` → `kod`
  - ```python kod bloku```

- **Formatlama Butonları**:
  - **𝐁**: Seçili metni kalın yapar
  - *𝐼*: Seçili metni italik yapar
  - 🔗: Link ekler
  - </> : Kod bloku ekler

### 📝 Örnek Yönetimi
- **Örnek Ekleme**: Sağ panelde "➕ Örnek Ekle"
- **Dil Desteği**: Python, JavaScript, HTML, CSS, vs.
- **Syntax Highlighting**: Kod örnekleri renkli görüntülenir
- **Hızlı Erişim**: Örneğe tıklayarak görüntüleyin

## 🛠️ Gelişmiş Özellikler

### 🔍 Arama
1. Sol üstteki arama kutusuna kelime yazın
2. "Ara" butonuna tıklayın
3. Sonuçlar tree'de vurgulanır

### 💾 Veri Yönetimi
- **Otomatik Kaydetme**: 30 saniyede bir otomatik kaydeder
- **Manuel Kaydetme**: Ctrl+S veya "💾" butonu
- **Yedekleme**: Veri > Backup Oluştur
- **İçe/Dışa Aktarma**: JSON formatında

### ⌨️ Klavye Kısayolları
- `Ctrl+S`: Kaydet
- `Ctrl+N`: Yeni kütüphane
- `Ctrl+O`: Dosya aç
- `Ctrl+F`: Arama
- `Ctrl+Q`: Çıkış

## 📂 Proje Yapısı Anlama

```
kutuphane/
├── main.py                 # Ana uygulama giriş noktası
├── requirements.txt        # Python bağımlılıkları
├── setup.py               # Kurulum scripti
├── src/                   # Kaynak kodlar
│   ├── models/            # Veri modelleri (Topic, Example, Library)
│   ├── views/             # UI bileşenleri (PySide6)
│   ├── viewmodels/        # İş mantığı (MVVM)
│   ├── services/          # Veri servisleri (JSON)
│   └── utils/             # Yardımcı fonksiyonlar
├── data/                  # Kütüphane verileri
│   └── library.json       # Ana veri dosyası
├── assets/               
│   ├── icons/             # Uygulama ikonları
│   └── styles/            # CSS stil dosyaları
└── tests/                 # Test dosyaları
```

## 🏗️ Mimari Anlama (MVVM)

### Model (Veri Katmanı)
```python
# src/models/library_models.py
class Library:     # Ana kütüphane
class Topic:       # Konu/başlık
class Example:     # Kod örnekleri
```

### View (UI Katmanı)
```python
# src/views/main_window.py
class MainWindow:  # Ana pencere
# src/views/components/
# - topic_tree_widget.py    # Sol ağaç görünümü
# - content_editor.py       # Orta içerik editörü
# - example_list_widget.py  # Sağ örnek listesi
```

### ViewModel (İş Mantığı)
```python
# src/viewmodels/library_viewmodel.py
class LibraryViewModel:  # UI ile Model arası köprü
```

### Service (Veri Servisi)
```python
# src/services/data_service.py
class DataService:  # JSON dosya yönetimi
```

## 🎨 Özelleştirme

### Stil Değişiklikleri
`assets/styles/main.qss` dosyasını düzenleyerek görünümü değiştirebilirsiniz:

```css
/* Tema rengi değiştirme */
QPushButton {
    background-color: #e74c3c;  /* Kırmızı tema */
}

/* Font değiştirme */
QTextEdit {
    font-family: "Comic Sans MS";
    font-size: 14pt;
}
```

### Yeni Özellik Ekleme
1. **Model**: `src/models/` altına yeni veri modeli
2. **Service**: `src/services/` altına veri işleme
3. **ViewModel**: `src/viewmodels/` altına iş mantığı
4. **View**: `src/views/` altına UI bileşeni

## 🐛 Sorun Giderme

### Uygulama Açılmıyor
```bash
# Bağımlılık kontrolü
pip list | grep PySide6

# Eksikse yükle
pip install PySide6
```

### Veri Kayboldu
1. `data/` klasöründe `library.json.bak` backup dosyasını arayın
2. `.bak` uzantısını silin ve dosya adını `library.json` yapın

### Import Hataları
```bash
# Python path'i kontrol et
python -c "import sys; print(sys.path)"

# Proje klasöründen çalıştırdığınızdan emin olun
cd kutuphane
python main.py
```

### Test Çalıştırma
```bash
# Tüm testler
python -m unittest tests.test_models

# Spesifik test
python -m unittest tests.test_models.TestLibraryModels.test_library_creation
```

## 📈 Gelecek Geliştirmeler

### Planlanan Özellikler
- [ ] SQLite veritabanı desteği
- [ ] Etiket sistemi
- [ ] Gelişmiş arama (regex, filtreler)
- [ ] Markdown preview
- [ ] Tema seçenekleri
- [ ] Plugin sistemi
- [ ] Export (PDF, HTML)
- [ ] Senkronizasyon (Google Drive, Dropbox)

### Katkıda Bulunma
1. Yeni özellik fikrini `tests/` klasöründe test et
2. MVVM mimarisine uygun kod yaz
3. Dokümantasyonu güncelle
4. Pull request gönder

## 📞 Destek

### Hata Bildirimi
Hata bulduğunuzda lütfen şu bilgileri paylaşın:
- İşletim sistemi
- Python sürümü
- Hatanın adımları
- Hata mesajı (varsa)

### İletişim
- GitHub Issues
- Email: [projenizin email adresi]

---

**💡 İpucu**: Bu kılavuzu uygulamanın kendi içinde de saklayabilirsiniz! "Yardım" konusu oluşturup içeriği kopyalayın. 😊
