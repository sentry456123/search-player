import re


def _search_string(text: str, pattern: str, regex=False) -> bool:
    if regex:
        try:
            return re.search(pattern, text) is not None
        except Exception:
            return False

    pos = 0
    for c in pattern:
        if c not in text[pos:]:
            return False
        pos = text.index(c, pos) + 1
    return True


class SearchEngine:

    def get_result(self) -> list[str]:
        result = []
        for name in self.source:
            if _search_string(name.lower(), self.buf.lower(), regex=self.regex):
                result.append(name)
        return result

    def __init__(self):
        self.regex = False
        self.buf = ''
        self.source: list[str] = []
