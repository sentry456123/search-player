from itertools import chain
import pygame
from pygame.font import Font


def truncline(text: str, font: Font, maxwidth: int) -> tuple[int, bool, str]:
    real = len(text)
    stext = text
    width = font.size(text)[0]
    cut = 0
    a = 0
    done = True
    while width > maxwidth:
        a += 1
        n = text.rsplit(None, a)[0]
        if stext == n:
            cut += 1
            stext = n[:-cut]
        else:
            stext = n
        width = font.size(stext)[0]
        real = len(stext)
        done = False
    return real, done, stext


def wrap_line(text: str, font: Font, maxwidth: int) -> list[str]:
    done = 0
    wrapped = []

    while not done:
        nl, done, stext = truncline(text, font, maxwidth)
        wrapped.append(stext.strip())
        text = text[nl:]
    return wrapped


def wrap_multiline(text: str, font: Font, maxwidth: int) -> list[str]:
    lines = chain(*(wrap_line(line, font, maxwidth)
                  for line in text.splitlines()))
    return list(lines)


def cut(text: str, font: Font, maxwidth: int) -> str:
    result = ''
    for c in text:
        result += c
        width = font.size(result)[0]
        if width > maxwidth:
            break
    return result


def cut_word(text: str, font: Font, maxwidth: int) -> str:
    real, done, stext = truncline(text, font, maxwidth)
    return stext.strip()


def _test():
    pygame.init()
    font = Font(None, 17)
    print(wrap_multiline('Now is the \ntime for all good men to come to the aid of their country', font, 120))

    print(cut('Today I bring you to the next level of the world', font, 120))

    pygame.quit()


if __name__ == '__main__':
    _test()
