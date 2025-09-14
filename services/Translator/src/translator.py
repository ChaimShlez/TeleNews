"""
מתרגם מהיר ואיכותי לעברית - תואם Python 3.13
Fast and High-Quality Hebrew Translator - Python 3.13 Compatible
"""
from langdetect import detect
import requests
import json
import re
from typing import Optional, Dict, List, Union
import time
from urllib.parse import quote


class HebrewTranslator:
    """
    מחלקה לתרגום מהיר ואיכותי לעברית
    """

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

        self.supported_languages = {
            'en': 'English',
            'es': 'Spanish',
            'fr': 'French',
            'de': 'German',
            'it': 'Italian',
            'pt': 'Portuguese',
            'ru': 'Russian',
            'ar': 'Arabic',
            'ja': 'Japanese',
            'ko': 'Korean',
            'zh': 'Chinese',
            'nl': 'Dutch',
            'sv': 'Swedish',
            'no': 'Norwegian',
            'da': 'Danish'
        }

    def detect_language(self, text: str) -> str:
        """
        מקבלת סטרינג ומחזירה את השפה המשוערת והסתברויות אפשריות.
        """
        try:
            main_lang = detect(text)
            return main_lang

        except Exception as e:
            return 'en'  # ברירת מחדל

    def translate_mymemory(self, text: str, source_lang: str = 'auto') -> Dict:
        """
        תרגום באמצעות MyMemory API (חינמי ויציב)
        """
        try:
            if source_lang == 'auto':
                source_lang = self.detect_language(text)

            # חלוקת טקסט ארוך לחלקים
            if len(text) > 500:
                return self._translate_long_text_mymemory(text, source_lang)

            url = "https://api.mymemory.translated.net/get"
            params = {
                'q': text,
                'langpair': f"{source_lang}|he",
                'de': 'user@example.com'  # מומלץ להוסיף מייל
            }

            response = self.session.get(url, params=params, timeout=10)
            data = response.json()

            if data['responseStatus'] == 200:
                translated = data['responseData']['translatedText']
                return {
                    'success': True,
                    'translated_text': translated,
                    'source_language': source_lang,
                    'confidence': data['responseData'].get('match', 0),
                    'method': 'MyMemory'
                }
            else:
                return {
                    'success': False,
                    'error': data.get('responseDetails', 'Unknown error'),
                    'method': 'MyMemory'
                }

        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'method': 'MyMemory'
            }

    def translate_libre(self, text: str, source_lang: str = 'auto') -> Dict:
        """
        תרגום באמצעות LibreTranslate (חינמי)
        """
        try:
            if source_lang == 'auto':
                source_lang = self.detect_language(text)

            url = "https://libretranslate.com/translate"
            data = {
                'q': text,
                'source': source_lang,
                'target': 'he',
                'format': 'text'
            }

            response = self.session.post(url, data=data, timeout=15)
            result = response.json()

            if 'translatedText' in result:
                return {
                    'success': True,
                    'translated_text': result['translatedText'],
                    'source_language': source_lang,
                    'method': 'LibreTranslate'
                }
            else:
                return {
                    'success': False,
                    'error': result.get('error', 'Unknown error'),
                    'method': 'LibreTranslate'
                }

        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'method': 'LibreTranslate'
            }

    def translate_microsoft(self, text: str, source_lang: str = 'auto') -> Dict:
        """
        תרגום באמצעות Microsoft Translator (דרך Bing)
        """
        try:
            if source_lang == 'auto':
                source_lang = self.detect_language(text)

            # Microsoft Translator דרך Bing
            url = "https://www.bing.com/ttranslatev3"

            data = {
                'fromLang': source_lang,
                'toLang': 'he',
                'text': text
            }

            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }

            response = self.session.post(url, data=data, headers=headers, timeout=10)

            if response.status_code == 200:
                # פירוק התגובה מ-Bing
                result_text = response.text
                if '"translationResponse"' in result_text:
                    import json
                    try:
                        # חיפוש התרגום בתגובה
                        start = result_text.find('"translationResponse"') + len('"translationResponse":"')
                        end = result_text.find('"', start)
                        translation = result_text[start:end].replace('\\u', '\\u')
                        translation = translation.encode().decode('unicode_escape')

                        return {
                            'success': True,
                            'translated_text': translation,
                            'source_language': source_lang,
                            'method': 'Microsoft Bing'
                        }
                    except:
                        pass

            return {
                'success': False,
                'error': 'Failed to parse Microsoft response',
                'method': 'Microsoft Bing'
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'method': 'Microsoft Bing'
            }

    def _translate_long_text_mymemory(self, text: str, source_lang: str) -> Dict:
        """
        תרגום טקסט ארוך על ידי חלוקה לחלקים
        """
        sentences = self._split_text(text)
        translated_parts = []

        for sentence in sentences:
            if sentence.strip():
                result = self.translate_mymemory(sentence.strip(), source_lang)
                if result['success']:
                    translated_parts.append(result['translated_text'])
                    time.sleep(0.1)  # מנע חסימה
                else:
                    translated_parts.append(sentence)  # שמירת המקור במקרה של שגיאה

        return {
            'success': True,
            'translated_text': ' '.join(translated_parts),
            'source_language': source_lang,
            'method': 'MyMemory (Long Text)'
        }

    def _split_text(self, text: str, max_length: int = 400) -> List[str]:
        """
        חלוקת טקסט למשפטים או לחלקים
        """
        # חלוקה על פי סימני פיסוק
        sentences = re.split(r'[.!?]+', text)

        parts = []
        current_part = ""

        for sentence in sentences:
            if len(current_part + sentence) < max_length:
                current_part += sentence + ". "
            else:
                if current_part:
                    parts.append(current_part.strip())
                current_part = sentence + ". "

        if current_part:
            parts.append(current_part.strip())

        return parts if parts else [text]

    def translate_with_fallback(self, text: str, source_lang: str = 'auto') -> Dict:
        """
        תרגום עם גיבוי מרובה
        """
        # רשימת השירותים לפי סדר עדיפות
        methods = [
            self.translate_mymemory,
            self.translate_libre,
            self.translate_microsoft
        ]

        for method in methods:
            try:
                result = method(text, source_lang)
                if result['success']:
                    return result
                else:
                    print(f"שירות {result['method']} נכשל: {result.get('error', 'Unknown error')}")
            except Exception as e:
                print(f"שגיאה בשירות {method.__name__}: {e}")
                continue

        return {
            'success': False,
            'error': 'כל השירותים נכשלו',
            'method': 'All methods failed'
        }

    def translate_batch(self, texts: List[str], source_lang: str = 'auto', delay: float = 0.2) -> List[Dict]:
        """
        תרגום קבצי עם השהיה למניעת חסימה
        """
        results = []
        total = len(texts)

        for i, text in enumerate(texts):
            print(f"מתרגם טקסט {i + 1}/{total}...")
            result = self.translate_with_fallback(text, source_lang)
            results.append(result)

            if i < total - 1:  # לא להשהות באיטרציה האחרונה
                time.sleep(delay)

        return results

    def translate_file(self, file_path: str, output_path: str = None, source_lang: str = 'auto') -> bool:
        """
        תרגום קובץ טקסט
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            result = self.translate_with_fallback(content, source_lang)

            if result['success']:
                output_path = output_path or file_path.replace('.txt', '_hebrew.txt')
                with open(output_path, 'w', encoding='utf-8') as file:
                    file.write(result['translated_text'])

                print(f"התרגום נשמר ב: {output_path}")
                return True
            else:
                print(f"שגיאה בתרגום: {result['error']}")
                return False

        except Exception as e:
            print(f"שגיאה בקריאת הקובץ: {e}")
            return False

    def get_supported_languages(self) -> Dict[str, str]:
        """
        החזרת רשימת השפות הנתמכות
        """
        return self.supported_languages.copy()


# פונקציית נוחות לשימוש מהיר
def quick_translate(text: str, source_lang: str = 'auto') -> str:
    """
    פונקציה מהירה לתרגום
    """
    translator = HebrewTranslator()
    result = translator.translate_with_fallback(text, source_lang)
    return result['translated_text'] if result['success'] else f"שגיאה: {result['error']}"








