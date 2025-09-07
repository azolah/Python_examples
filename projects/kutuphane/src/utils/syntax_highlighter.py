"""
Syntax highlighting yardımcı fonksiyonları
"""

from pygments import highlight
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.formatters import HtmlFormatter
from pygments.util import ClassNotFound


class SyntaxHighlighter:
    """Kod syntax highlighting için yardımcı sınıf"""
    
    def __init__(self):
        self.formatter = HtmlFormatter(
            style='default',
            noclasses=True,
            linenos=False
        )
    
    def highlight_code(self, code: str, language: str = 'text') -> str:
        """
        Verilen kodu syntax highlighting ile formatlar
        
        Args:
            code: Formatlanacak kod
            language: Programlama dili (python, javascript, etc.)
            
        Returns:
            str: HTML formatında highlight edilmiş kod
        """
        if not code.strip():
            return code
        
        try:
            if language.lower() == 'text' or language.lower() == 'plain':
                return f"<pre>{code}</pre>"
            
            lexer = get_lexer_by_name(language.lower())
            highlighted = highlight(code, lexer, self.formatter)
            return highlighted
            
        except ClassNotFound:
            # Bilinmeyen dil, düz metin olarak göster
            return f"<pre>{code}</pre>"
        except Exception:
            # Hata durumunda düz metin döndür
            return f"<pre>{code}</pre>"
    
    def guess_language(self, code: str) -> str:
        """
        Kod içeriğinden programlama dilini tahmin eder
        
        Args:
            code: Analiz edilecek kod
            
        Returns:
            str: Tahmin edilen dil
        """
        try:
            lexer = guess_lexer(code)
            return lexer.name.lower()
        except:
            return 'text'
    
    def get_supported_languages(self) -> list:
        """
        Desteklenen programlama dillerinin listesini döndürür
        
        Returns:
            list: Desteklenen diller
        """
        common_languages = [
            'python', 'javascript', 'java', 'c++', 'c', 'c#',
            'html', 'css', 'sql', 'bash', 'powershell',
            'json', 'xml', 'yaml', 'markdown', 'text'
        ]
        return common_languages
