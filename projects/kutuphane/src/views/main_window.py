"""
Ana uygulama penceresi
"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QSplitter, QTreeView, QTextEdit, QListWidget, 
    QPushButton, QLineEdit, QLabel, QMenuBar, QMenu,
    QToolBar, QStatusBar, QMessageBox, QInputDialog,
    QFileDialog, QListWidgetItem, QHeaderView
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QAction, QIcon, QFont
from typing import Optional

from ..viewmodels.library_viewmodel import LibraryViewModel
from .components.topic_tree_widget import TopicTreeWidget
from .components.content_editor import ContentEditor
from .components.example_list_widget import ExampleListWidget


class MainWindow(QMainWindow):
    """Ana uygulama penceresi - 3 panel tasarım"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kişisel Kütüphane v1.0")
        self.setGeometry(100, 100, 1400, 800)
        
        # ViewModel
        self.view_model = LibraryViewModel()
        
        # UI bileşenlerini oluştur
        self._setup_ui()
        self._setup_menu_bar()
        self._setup_tool_bar()
        self._setup_status_bar()
        self._connect_signals()
        
        # Auto-save timer
        self._auto_save_timer = QTimer()
        self._auto_save_timer.timeout.connect(self._auto_save)
        self._auto_save_timer.start(30000)  # 30 saniyede bir kaydet
        
        # Başlangıçta veriyi yükle
        self.view_model.load_library()
    
    def _setup_ui(self):
        """Ana UI layout'unu oluşturur"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Ana splitter (3 panel)
        main_splitter = QSplitter(Qt.Horizontal)
        central_widget.layout = QHBoxLayout(central_widget)
        central_widget.layout.addWidget(main_splitter)
        
        # Sol panel - Konu ağacı
        left_panel = self._create_left_panel()
        main_splitter.addWidget(left_panel)
        
        # Orta panel - İçerik editörü
        middle_panel = self._create_middle_panel()
        main_splitter.addWidget(middle_panel)
        
        # Sağ panel - Örnekler
        right_panel = self._create_right_panel()
        main_splitter.addWidget(right_panel)
        
        # Panel boyutlarını ayarla (25% - 50% - 25%)
        main_splitter.setSizes([350, 700, 350])
        main_splitter.setStretchFactor(0, 0)  # Sol panel sabit
        main_splitter.setStretchFactor(1, 1)  # Orta panel esnek
        main_splitter.setStretchFactor(2, 0)  # Sağ panel sabit
    
    def _create_left_panel(self) -> QWidget:
        """Sol panel - Konu ağacı ve arama"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # Arama kutusu
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Konularda ara...")
        self.search_button = QPushButton("Ara")
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_button)
        layout.addLayout(search_layout)
        
        # Konu ağacı
        self.topic_tree = TopicTreeWidget()
        layout.addWidget(self.topic_tree)
        
        # Konu yönetim butonları
        button_layout = QHBoxLayout()
        self.add_topic_btn = QPushButton("➕ Konu Ekle")
        self.edit_topic_btn = QPushButton("✏️ Düzenle")
        self.delete_topic_btn = QPushButton("🗑️ Sil")
        
        button_layout.addWidget(self.add_topic_btn)
        button_layout.addWidget(self.edit_topic_btn)
        button_layout.addWidget(self.delete_topic_btn)
        layout.addLayout(button_layout)
        
        return panel
    
    def _create_middle_panel(self) -> QWidget:
        """Orta panel - İçerik editörü"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # Başlık ve breadcrumb
        header_layout = QVBoxLayout()
        self.topic_title_label = QLabel("Konu seçiniz")
        self.topic_title_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.breadcrumb_label = QLabel("")
        self.breadcrumb_label.setStyleSheet("color: #666; font-size: 12px;")
        
        header_layout.addWidget(self.topic_title_label)
        header_layout.addWidget(self.breadcrumb_label)
        layout.addLayout(header_layout)
        
        # İçerik editörü
        self.content_editor = ContentEditor()
        layout.addWidget(self.content_editor)
        
        # İçerik yönetim butonları
        content_button_layout = QHBoxLayout()
        self.save_content_btn = QPushButton("💾 Kaydet")
        self.format_bold_btn = QPushButton("𝐁")
        self.format_italic_btn = QPushButton("𝐼")
        self.add_link_btn = QPushButton("🔗 Link")
        self.add_code_btn = QPushButton("</> Kod")
        
        self.save_content_btn.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; }")
        
        content_button_layout.addWidget(self.save_content_btn)
        content_button_layout.addStretch()
        content_button_layout.addWidget(self.format_bold_btn)
        content_button_layout.addWidget(self.format_italic_btn)
        content_button_layout.addWidget(self.add_link_btn)
        content_button_layout.addWidget(self.add_code_btn)
        
        layout.addLayout(content_button_layout)
        
        return panel
    
    def _create_right_panel(self) -> QWidget:
        """Sağ panel - Örnekler"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # Başlık
        examples_label = QLabel("Örnekler")
        examples_label.setFont(QFont("Arial", 14, QFont.Bold))
        layout.addWidget(examples_label)
        
        # Örnek listesi
        self.example_list = ExampleListWidget()
        layout.addWidget(self.example_list)
        
        # Örnek yönetim butonları
        example_button_layout = QHBoxLayout()
        self.add_example_btn = QPushButton("➕ Örnek Ekle")
        self.edit_example_btn = QPushButton("✏️ Düzenle")
        self.delete_example_btn = QPushButton("🗑️ Sil")
        
        example_button_layout.addWidget(self.add_example_btn)
        example_button_layout.addWidget(self.edit_example_btn)
        example_button_layout.addWidget(self.delete_example_btn)
        layout.addLayout(example_button_layout)
        
        # Seçili örnek görüntüleme alanı
        self.example_viewer = QTextEdit()
        self.example_viewer.setReadOnly(True)
        self.example_viewer.setMaximumHeight(200)
        layout.addWidget(self.example_viewer)
        
        return panel
    
    def _setup_menu_bar(self):
        """Menü çubuğunu oluşturur"""
        menubar = self.menuBar()
        
        # Dosya menüsü
        file_menu = menubar.addMenu("Dosya")
        
        new_action = QAction("Yeni Kütüphane", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self._new_library)
        file_menu.addAction(new_action)
        
        open_action = QAction("Aç...", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self._open_file)
        file_menu.addAction(open_action)
        
        save_action = QAction("Kaydet", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self._save_file)
        file_menu.addAction(save_action)
        
        file_menu.addSeparator()
        
        export_action = QAction("Dışa Aktar...", self)
        export_action.triggered.connect(self._export_data)
        file_menu.addAction(export_action)
        
        import_action = QAction("İçe Aktar...", self)
        import_action.triggered.connect(self._import_data)
        file_menu.addAction(import_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Çıkış", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Düzen menüsü
        edit_menu = menubar.addMenu("Düzen")
        
        search_action = QAction("Ara...", self)
        search_action.setShortcut("Ctrl+F")
        search_action.triggered.connect(self._focus_search)
        edit_menu.addAction(search_action)
        
        # Yardım menüsü
        help_menu = menubar.addMenu("Yardım")
        
        about_action = QAction("Hakkında", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)
    
    def _setup_tool_bar(self):
        """Araç çubuğunu oluşturur"""
        toolbar = self.addToolBar("Ana")
        
        # Hızlı erişim butonları
        save_action = QAction("💾", self)
        save_action.setToolTip("Kaydet (Ctrl+S)")
        save_action.triggered.connect(self._save_file)
        toolbar.addAction(save_action)
        
        toolbar.addSeparator()
        
        add_topic_action = QAction("➕", self)
        add_topic_action.setToolTip("Yeni Konu Ekle")
        add_topic_action.triggered.connect(self._add_topic)
        toolbar.addAction(add_topic_action)
        
        add_example_action = QAction("📝", self)
        add_example_action.setToolTip("Yeni Örnek Ekle")
        add_example_action.triggered.connect(self._add_example)
        toolbar.addAction(add_example_action)
    
    def _setup_status_bar(self):
        """Durum çubuğunu oluşturur"""
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("Hazır")
    
    def _connect_signals(self):
        """Sinyal bağlantılarını kurar"""
        # ViewModel sinyalleri
        self.view_model.library_loaded.connect(self._on_library_loaded)
        self.view_model.library_saved.connect(self._on_library_saved)
        self.view_model.topic_selected.connect(self._on_topic_selected)
        self.view_model.example_selected.connect(self._on_example_selected)
        self.view_model.data_changed.connect(self._on_data_changed)
        self.view_model.error_occurred.connect(self._on_error)
        
        # UI sinyalleri
        self.search_button.clicked.connect(self._search_topics)
        self.search_input.returnPressed.connect(self._search_topics)
        
        self.add_topic_btn.clicked.connect(self._add_topic)
        self.edit_topic_btn.clicked.connect(self._edit_topic)
        self.delete_topic_btn.clicked.connect(self._delete_topic)
        
        self.save_content_btn.clicked.connect(self._save_content)
        self.format_bold_btn.clicked.connect(self.content_editor.toggle_bold)
        self.format_italic_btn.clicked.connect(self.content_editor.toggle_italic)
        self.add_link_btn.clicked.connect(self.content_editor.insert_link)
        self.add_code_btn.clicked.connect(self.content_editor.insert_code_block)
        
        self.add_example_btn.clicked.connect(self._add_example)
        self.edit_example_btn.clicked.connect(self._edit_example)
        self.delete_example_btn.clicked.connect(self._delete_example)
        
        # Tree selection
        self.topic_tree.topic_selected.connect(self.view_model.select_topic_by_id)
        
        # Example selection
        self.example_list.example_selected.connect(self.view_model.select_example_by_id)
    
    # Slot methods - UI olaylarına tepki
    def _on_library_loaded(self):
        """Kütüphane yüklendiğinde çağrılır"""
        self.topic_tree.set_model(self.view_model.get_tree_model())
        self.status_bar.showMessage("Kütüphane yüklendi")
    
    def _on_library_saved(self, success: bool):
        """Kütüphane kaydedildiğinde çağrılır"""
        if success:
            self.status_bar.showMessage("Kaydedildi", 2000)
        else:
            self.status_bar.showMessage("Kaydetme hatası!", 5000)
    
    def _on_topic_selected(self, topic_id: str):
        """Konu seçildiğinde çağrılır"""
        self.topic_title_label.setText(self.view_model.current_topic_title)
        self.content_editor.set_content(self.view_model.current_topic_content)
        
        # Breadcrumb güncelle
        hierarchy = self.view_model.get_topic_hierarchy(topic_id)
        breadcrumb = " > ".join([item['title'] for item in hierarchy])
        self.breadcrumb_label.setText(breadcrumb)
        
        # Örnek listesini güncelle
        examples = self.view_model.get_current_topic_examples()
        self.example_list.update_examples(examples)
        
        self.status_bar.showMessage(f"Konu seçildi: {self.view_model.current_topic_title}")
    
    def _on_example_selected(self, example_id: str):
        """Örnek seçildiğinde çağrılır"""
        content = f"**{self.view_model.current_example_name}**\n\n"
        content += f"Dil: {self.view_model.current_example_language}\n\n"
        content += "```" + self.view_model.current_example_language + "\n"
        content += self.view_model.current_example_content + "\n```"
        
        self.example_viewer.setMarkdown(content)
        self.status_bar.showMessage(f"Örnek seçildi: {self.view_model.current_example_name}")
    
    def _on_data_changed(self):
        """Veri değiştiğinde çağrılır"""
        self.setWindowTitle("Kişisel Kütüphane v1.0 *")  # * ile değişiklik belirt
    
    def _on_error(self, message: str):
        """Hata oluştuğunda çağrılır"""
        QMessageBox.critical(self, "Hata", message)
        self.status_bar.showMessage(f"Hata: {message}", 5000)
    
    # Action methods
    def _new_library(self):
        """Yeni kütüphane oluşturur"""
        reply = QMessageBox.question(
            self, "Yeni Kütüphane", 
            "Mevcut değişiklikler kaybolacak. Devam edilsin mi?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # Yeni kütüphane oluşturma mantığı burada
            pass
    
    def _open_file(self):
        """Dosya açma diyalogu"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Kütüphane Dosyası Aç", "", "JSON Files (*.json)"
        )
        
        if file_path:
            if self.view_model.import_data(file_path):
                self.setWindowTitle("Kişisel Kütüphane v1.0")
    
    def _save_file(self):
        """Mevcut kütüphaneyi kaydet"""
        self.view_model.save_library()
        self.setWindowTitle("Kişisel Kütüphane v1.0")
    
    def _export_data(self):
        """Veri dışa aktarma"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Veri Dışa Aktar", "", "JSON Files (*.json)"
        )
        
        if file_path:
            self.view_model.export_data(file_path)
    
    def _import_data(self):
        """Veri içe aktarma"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Veri İçe Aktar", "", "JSON Files (*.json)"
        )
        
        if file_path:
            self.view_model.import_data(file_path)
    
    def _focus_search(self):
        """Arama kutusuna odaklan"""
        self.search_input.setFocus()
        self.search_input.selectAll()
    
    def _search_topics(self):
        """Konu arama"""
        query = self.search_input.text().strip()
        if query:
            results = self.view_model.search_topics(query)
            # Arama sonuçlarını göster (basitleştirilmiş)
            if results:
                self.status_bar.showMessage(f"{len(results)} sonuç bulundu")
            else:
                self.status_bar.showMessage("Sonuç bulunamadı")
    
    def _add_topic(self):
        """Yeni konu ekle"""
        title, ok = QInputDialog.getText(self, "Yeni Konu", "Konu başlığı:")
        if ok and title.strip():
            # Şu anda seçili konunun ID'sini al (varsa alt konu olarak ekle)
            parent_id = None
            if hasattr(self.topic_tree, 'get_selected_topic_id'):
                parent_id = self.topic_tree.get_selected_topic_id()
            
            topic_id = self.view_model.add_new_topic(title.strip(), parent_id)
            if topic_id:
                self.status_bar.showMessage(f"Konu eklendi: {title}")
    
    def _edit_topic(self):
        """Seçili konu düzenle"""
        # Implementation needed
        pass
    
    def _delete_topic(self):
        """Seçili konu sil"""
        # Implementation needed
        pass
    
    def _save_content(self):
        """İçerik kaydet"""
        if hasattr(self.topic_tree, 'get_selected_topic_id'):
            topic_id = self.topic_tree.get_selected_topic_id()
            if topic_id:
                content = self.content_editor.get_content()
                self.view_model.update_topic_content(topic_id, content)
    
    def _add_example(self):
        """Yeni örnek ekle"""
        name, ok = QInputDialog.getText(self, "Yeni Örnek", "Örnek adı:")
        if ok and name.strip():
            example_id = self.view_model.add_new_example(name.strip(), "", "python")
            if example_id:
                self.status_bar.showMessage(f"Örnek eklendi: {name}")
    
    def _edit_example(self):
        """Seçili örnek düzenle"""
        # Implementation needed
        pass
    
    def _delete_example(self):
        """Seçili örnek sil"""
        # Implementation needed
        pass
    
    def _auto_save(self):
        """Otomatik kaydetme"""
        self.view_model.save_library()
    
    def _show_about(self):
        """Hakkında diyalogu"""
        QMessageBox.about(
            self, "Hakkında",
            "Kişisel Kütüphane v1.0\n\n"
            "Öğrendiğiniz bilgileri organize etmek için\n"
            "geliştirilmiş masaüstü uygulaması.\n\n"
            "Python + PySide6 ile geliştirilmiştir."
        )
    
    def closeEvent(self, event):
        """Uygulama kapatılırken"""
        # Son değişiklikleri kaydet
        self.view_model.save_library()
        event.accept()
