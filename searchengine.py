import re


def _search_string(text: str, pattern: str, regex=False) -> bool:
    if regex:
        try:
            return re.search(pattern, text) is not None
        except Exception as e:
            return False

    text_pos = 0
    for pattern_char in pattern:
        if pattern_char not in text[text_pos:]:
            return False
        text_pos = text.index(pattern_char, text_pos) + 1
    return True


class SearchEngine:

    def sort_words(self, new_words: list[str]):
        self.words = []
        for word in new_words:
            if _search_string(word.lower(), self.buf.lower(), regex=self.regex):
                self.words.append(word)

    def set_selection(self, selection):
        self.selection = selection
        if self.selection >= len(self.words):
            self.selection = len(self.words) - 1
        if self.selection < 0:
            self.selection = 0

    def move_selection(self, offset: int):
        self.set_selection(self.selection + offset)

    def get_selected(self) -> str:
        if len(self.words) == 0:
            return ''
        return self.words[self.selection]

    def __init__(self):
        self.words: list[str] = []
        self.selection = 0
        self.buf = ''
        self.regex = False
