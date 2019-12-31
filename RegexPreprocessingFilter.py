from telegram.ext import BaseFilter
import re
import unicodedata

class RegexPreprocessingFilter(BaseFilter):
    def __init__(self, pattern):
        self.pattern = pattern
    
    @staticmethod
    def _remove_diacritics(text):
        """
        Returns a string with all diacritics (aka non-spacing marks) removed.
        For example "Héllô" will become "Hello".
        Useful for comparing strings in an accent-insensitive fashion.
        """
        normalized = unicodedata.normalize("NFKD", text)
        return "".join(c for c in normalized if unicodedata.category(c) != "Mn")

    def filter(self, message):
        if message.text:
            text = self._remove_diacritics(message.text)
            match = self.pattern.search(text)
            return match is not None
