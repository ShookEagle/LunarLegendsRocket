import json
import os
from config.settings import LANG_PATH, LANGUAGE

def load_language_file(language):
    file_path = os.path.join(LANG_PATH, f"{language}.json")
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

class Localizer:
    def __init__(self, language=LANGUAGE):
        self.language = language
        self.locale = load_language_file(language)

    def print_local(self, key, **kwargs):
        message = self.locale.get(key, f"Missing message for key: {key}")
        print(message.format(**kwargs))

    def print_local_error(self, key, **kwargs):
        message = self.locale.get(key, f"Missing message for key: {key}")
        print("ERROR: " + message.format(**kwargs))

# Global shared instance
localizer = Localizer()