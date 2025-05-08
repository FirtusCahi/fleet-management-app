import json
import os

class LanguageManager:
    def __init__(self, default_lang='fr'):
        self.default_lang = default_lang
        self.current_lang = default_lang
        self.translations = self._load_translations()

    def _load_translations(self):
        translations = {}
        lang_dir = os.path.join(os.path.dirname(__file__), 'translations')
        for filename in os.listdir(lang_dir):
            if filename.endswith('.json'):
                lang_code = filename[:-5]
                filepath = os.path.join(lang_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        translations[lang_code] = json.load(f)
                except FileNotFoundError:
                    print(f"Erreur: Fichier de langue non trouvé: {filepath}")
                except json.JSONDecodeError:
                    print(f"Erreur: Impossible de décoder le JSON dans: {filepath}")
        return translations

    def switch_language(self, lang_code):
        if lang_code in self.translations:
            self.current_lang = lang_code
            return True
        else:
            print(f"Langue non supportée: {lang_code}")
            return False

    def get(self, key, default=None):
        if self.current_lang in self.translations and key in self.translations[self.current_lang]:
            return self.translations[self.current_lang][key]
        elif self.default_lang in self.translations and key in self.translations[self.default_lang]:
            return self.translations[self.default_lang][key]
            return default