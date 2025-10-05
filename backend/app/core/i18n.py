"""Internationalization (i18n) support."""
from typing import Any
from pathlib import Path
import json
from app.core.config import settings


class Translator:
    """Simple translation system for backend messages."""

    def __init__(self, locale: str = "en") -> None:
        self.locale = locale if locale in settings.SUPPORTED_LOCALES else settings.DEFAULT_LOCALE
        self.translations: dict[str, Any] = {}
        self._load_translations()

    def _load_translations(self) -> None:
        """Load translation file for current locale."""
        locale_file = Path(__file__).parent.parent / "locales" / f"{self.locale}.json"

        if locale_file.exists():
            with open(locale_file, "r", encoding="utf-8") as f:
                self.translations = json.load(f)

    def translate(self, key: str, **kwargs: Any) -> str:
        """
        Translate a key with optional parameters.

        Args:
            key: Translation key (e.g., "errors.invalid_email")
            **kwargs: Variables to interpolate

        Returns:
            Translated string

        Example:
            ```python
            t = Translator("en")
            message = t.translate("errors.user_not_found", user_id="123")
            ```
        """
        # Navigate through nested keys
        keys = key.split(".")
        value = self.translations

        for k in keys:
            if isinstance(value, dict):
                value = value.get(k, key)
            else:
                return key

        # If not found, return key itself
        if not isinstance(value, str):
            return key

        # Interpolate variables
        try:
            return value.format(**kwargs)
        except KeyError:
            return value

    def __call__(self, key: str, **kwargs: Any) -> str:
        """Shorthand for translate."""
        return self.translate(key, **kwargs)


# Translation cache
_translators: dict[str, Translator] = {}


def get_translator(locale: str = "en") -> Translator:
    """
    Get translator instance for locale.

    Args:
        locale: Locale code (en, ru, es, zh, ar)

    Returns:
        Translator instance
    """
    if locale not in _translators:
        _translators[locale] = Translator(locale)
    return _translators[locale]


def get_locale_from_header(accept_language: str | None) -> str:
    """
    Extract preferred locale from Accept-Language header.

    Args:
        accept_language: Accept-Language header value

    Returns:
        Locale code
    """
    if not accept_language:
        return settings.DEFAULT_LOCALE

    # Parse Accept-Language header (e.g., "en-US,en;q=0.9,ru;q=0.8")
    languages = []
    for lang in accept_language.split(","):
        parts = lang.strip().split(";")
        code = parts[0].split("-")[0].lower()
        quality = 1.0

        if len(parts) > 1:
            try:
                quality = float(parts[1].split("=")[1])
            except (IndexError, ValueError):
                pass

        languages.append((code, quality))

    # Sort by quality
    languages.sort(key=lambda x: x[1], reverse=True)

    # Return first supported language
    for code, _ in languages:
        if code in settings.SUPPORTED_LOCALES:
            return code

    return settings.DEFAULT_LOCALE
