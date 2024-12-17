import json
import os
from config.settings import LOCALE_PATH

class Localizer:
    def __init__(self, language="en"):
        self.language = language
        self.messages = self.load_language_file(language)

    def load_language_file(self, language):
        """
        Load the JSON file for the specified language.
        """
        file_path = os.path.join(LOCALE_PATH, f"{language}.json")
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Localization file for '{language}' not found. Falling back to English.")
            return self.load_language_file("en")
        except json.JSONDecodeError as e:
            print(f"Error decoding localization file: {e}")
            return {}

    def get_message(self, local, **kwargs):
        """
        Retrieve the localized message for the given key and format with kwargs.
        """
        template = self.messages.get(local, f"Missing message for key: {local}")
        return template.format(**kwargs)

    def print_localized(self, local, **kwargs):
        template = self.messages.get(local, f"Missing message for key: {local}")
        print(template.format(**kwargs))