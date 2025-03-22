import json
import os
from config.settings import LANG_PATH


def load_language_file(language):
    file_path = os.path.join(LANG_PATH, f"{language}.json")
    with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)


class Localizer:
    def __init__(self, language="en"):
        self.language = language
        self.locale = load_language_file(language)

    def print_local(self, key, **kwargs):
        localized_message = self.locale.get(key, f"Missing message for key: {key}")
        print(localized_message.format(**kwargs))

    def print_local_error(self, key, **kwargs):
        localized_message = self.locale.get(key, f"Missing message for key: {key}")
        error_message = localized_message.replace("%error%", self.locale.get("error"))
        print(error_message.format(**kwargs))