from typing import Optional
from config import TARGET_LANG
import socket

try:
    from googletrans import Translator as GoogleTranslator
    has_google = True
except ImportError:
    has_google = False

try:
    import argostranslate.package, argostranslate.translate
    has_argos = True
except ImportError:
    has_argos = False

class TextTranslator:
    def __init__(self, dest_lang: str = TARGET_LANG):
        self.dest_lang = dest_lang
        self.online = self._check_internet()
        self.translator = None

        if self.online and has_google:
            self.mode = "google"
            self.translator = GoogleTranslator(service_urls=["translate.google.com"])
        elif has_argos:
            self.mode = "argos"
            installed = argostranslate.translate.get_installed_languages()
            self.source_lang, self.target_lang = self._find_languages("en", dest_lang, installed)
        else:
            self.mode = "none"

    def _check_internet(self) -> bool:
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=2)
            return True
        except OSError:
            return False

    def _find_languages(self, from_code, to_code, langs):
        for lang in langs:
            for to_lang in langs:
                if lang.code == from_code and to_lang.code == to_code:
                    return lang, to_lang
        return None, None

    def translate(self, text: str) -> Optional[str]:
        if self.mode == "google":
            try:
                return self.translator.translate(text, dest=self.dest_lang).text
            except Exception:
                return None
        elif self.mode == "argos" and self.source_lang and self.target_lang:
            return self.source_lang.get_translation(self.target_lang).translate(text)
        else:
            return None
