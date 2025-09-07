"""
Markdown işleme yardımcı fonksiyonları
"""

import re
from typing import Dict, List


class MarkdownProcessor:
    """Basit markdown işleme için yardımcı sınıf"""
    
    def __init__(self):
        # Basit markdown pattern'ları
        self.patterns = {
            'bold': r'\*\*(.*?)\*\*',
            'italic': r'\*(.*?)\*',
            'code_inline': r'`(.*?)`',
            'code_block': r'```(\w+)?\n(.*?)\n```',
            'link': r'\[(.*?)\]\((.*?)\)',
            'heading1': r'^# (.*?)$',
            'heading2': r'^## (.*?)$',
            'heading3': r'^### (.*?)$',
            'list_item': r'^\* (.*?)$',
            'list_item_bullet': r'^• (.*?)$'
        }
    
    def to_html(self, markdown_text: str) -> str:
        """
        Markdown metnini HTML'e çevirir
        
        Args:
            markdown_text: Markdown formatında metin
            
        Returns:
            str: HTML formatında metin
        """
        if not markdown_text:
            return ""
        
        html = markdown_text
        
        # Kod blokları (önce işlenmeli)
        html = re.sub(
            self.patterns['code_block'],
            r'<pre><code class="language-\1">\2</code></pre>',
            html,
            flags=re.MULTILINE | re.DOTALL
        )
        
        # Başlıklar
        html = re.sub(self.patterns['heading1'], r'<h1>\1</h1>', html, flags=re.MULTILINE)
        html = re.sub(self.patterns['heading2'], r'<h2>\1</h2>', html, flags=re.MULTILINE)
        html = re.sub(self.patterns['heading3'], r'<h3>\1</h3>', html, flags=re.MULTILINE)
        
        # Bold ve italic
        html = re.sub(self.patterns['bold'], r'<strong>\1</strong>', html)
        html = re.sub(self.patterns['italic'], r'<em>\1</em>', html)
        
        # Inline kod
        html = re.sub(self.patterns['code_inline'], r'<code>\1</code>', html)
        
        # Linkler
        html = re.sub(self.patterns['link'], r'<a href="\2">\1</a>', html)
        
        # Liste öğeleri
        html = re.sub(self.patterns['list_item'], r'<li>\1</li>', html, flags=re.MULTILINE)
        html = re.sub(self.patterns['list_item_bullet'], r'<li>\1</li>', html, flags=re.MULTILINE)
        
        # Paragraflar
        paragraphs = html.split('\n\n')
        formatted_paragraphs = []
        
        for paragraph in paragraphs:
            paragraph = paragraph.strip()
            if paragraph:
                # Başlık, liste öğesi veya kod bloku değilse paragraf olarak sar
                if not (paragraph.startswith('<h') or 
                       paragraph.startswith('<li>') or 
                       paragraph.startswith('<pre>') or
                       paragraph.startswith('<ul>') or
                       paragraph.startswith('<ol>')):
                    paragraph = f'<p>{paragraph}</p>'
                formatted_paragraphs.append(paragraph)
        
        html = '\n'.join(formatted_paragraphs)
        
        # Satır sonlarını <br> ile değiştir
        html = html.replace('\n', '<br>')
        
        return html
    
    def to_plain_text(self, markdown_text: str) -> str:
        """
        Markdown metninden düz metin çıkarır
        
        Args:
            markdown_text: Markdown formatında metin
            
        Returns:
            str: Düz metin
        """
        if not markdown_text:
            return ""
        
        text = markdown_text
        
        # Markdown işaretlerini kaldır
        text = re.sub(self.patterns['bold'], r'\1', text)
        text = re.sub(self.patterns['italic'], r'\1', text)
        text = re.sub(self.patterns['code_inline'], r'\1', text)
        text = re.sub(self.patterns['code_block'], r'\2', text, flags=re.MULTILINE | re.DOTALL)
        text = re.sub(self.patterns['link'], r'\1', text)
        text = re.sub(self.patterns['heading1'], r'\1', text, flags=re.MULTILINE)
        text = re.sub(self.patterns['heading2'], r'\1', text, flags=re.MULTILINE)
        text = re.sub(self.patterns['heading3'], r'\1', text, flags=re.MULTILINE)
        text = re.sub(self.patterns['list_item'], r'\1', text, flags=re.MULTILINE)
        text = re.sub(self.patterns['list_item_bullet'], r'\1', text, flags=re.MULTILINE)
        
        return text.strip()
    
    def extract_links(self, markdown_text: str) -> List[Dict[str, str]]:
        """
        Markdown metninden linkleri çıkarır
        
        Args:
            markdown_text: Markdown formatında metin
            
        Returns:
            List[Dict]: Link listesi [{'text': 'link_text', 'url': 'link_url'}]
        """
        if not markdown_text:
            return []
        
        links = []
        matches = re.finditer(self.patterns['link'], markdown_text)
        
        for match in matches:
            links.append({
                'text': match.group(1),
                'url': match.group(2)
            })
        
        return links
    
    def get_word_count(self, markdown_text: str) -> int:
        """
        Markdown metnindeki kelime sayısını döndürür
        
        Args:
            markdown_text: Markdown formatında metin
            
        Returns:
            int: Kelime sayısı
        """
        plain_text = self.to_plain_text(markdown_text)
        words = plain_text.split()
        return len(words)
    
    def get_reading_time(self, markdown_text: str, words_per_minute: int = 200) -> int:
        """
        Tahmini okuma süresini dakika cinsinden döndürür
        
        Args:
            markdown_text: Markdown formatında metin
            words_per_minute: Dakika başına okunan kelime sayısı
            
        Returns:
            int: Tahmini okuma süresi (dakika)
        """
        word_count = self.get_word_count(markdown_text)
        reading_time = max(1, round(word_count / words_per_minute))
        return reading_time
