import vlc
import os
import pygame
import numpy


FONT_SIZE = 40

player: vlc.MediaPlayer = vlc.MediaPlayer()
files = os.listdir()
selection = 0
font: pygame.font.Font
window: pygame.Surface


def search_string(text: str, pattern: str) -> bool:
    text_index = 0
    for pchar in pattern:
        matched = False
        for tchar in text[text_index:]:
            if pchar == tchar:
                matched = True
                break
            text_index += 1
        if not matched:
            return False
    return True


def parent_dir():
    global files
    global input_buffer
    global selection

    os.chdir('../')
    files = os.listdir()
    input_buffer = ""
    selection = 0


def open_file():
    global files
    global input_buffer
    global selection

    if len(files) == 0:
        return

    next_path = files[selection]
    if os.path.isdir(next_path):
        os.chdir(next_path)
        files = os.listdir()
        input_buffer = ""
        selection = 0
    else:
        player.set_mrl(next_path)
        player.play()


def up():
    global selection

    selection -= 1
    selection = numpy.clip(selection, 0, len(files) - 1)


def down():
    global selection

    selection += 1
    selection = numpy.clip(selection, 0, len(files) - 1)


def render_text(text: str, position):
    font_image = font.render(text, True, (255, 255, 255))
    window.blit(font_image, position)


def main():
    global files
    global selection
    global font
    global window

    input_buffer = ""

    running = True
    player.audio_set_volume(100)

    pygame.init()
    window = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Search Player")
    font = pygame.font.SysFont(None, FONT_SIZE)

    while running:
        event = pygame.event.wait()

        if event.type == pygame.QUIT:
            running = False
        match event.type:
            case pygame.QUIT: running = False
            case pygame.KEYDOWN:
                if not event.mod & pygame.KMOD_CTRL:
                    match event.key:
                        case pygame.K_ESCAPE:
                            parent_dir()
                        case pygame.K_RETURN:
                            open_file()
                        case pygame.K_UP:
                            up()
                        case pygame.K_DOWN:
                            down()
                        case pygame.K_LEFT:
                            player.pause()
                        case pygame.K_RIGHT:
                            player.play()
                        case pygame.K_BACKSPACE:
                            input_buffer = input_buffer[:-1]
                            selection = 0
                        case _:
                            input_buffer += event.unicode
                            selection = 0
                
        files = []
        for file in os.listdir():
            if search_string(file.lower(), input_buffer.lower()):
                files.append(file)

        window.fill((30, 30, 30))

        starting_point = 0
        if selection >= window.get_height() / FONT_SIZE - 1:
            starting_point = -selection + window.get_height() / FONT_SIZE - 2
        
        pygame.draw.rect(window, (225, 30, 30), (0, (selection + 1 + starting_point) * FONT_SIZE, window.get_width(), FONT_SIZE))
        for i, filename in enumerate(files):
            render_text(filename, (0, (i + 1 + starting_point) * FONT_SIZE))

        pygame.draw.rect(window, (30, 30, 225), (0, 0, window.get_width(), FONT_SIZE))
        render_text(input_buffer, (0, 0))

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()