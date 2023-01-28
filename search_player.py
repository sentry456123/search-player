import vlc
import os
import pygame
import numpy


player: vlc.MediaPlayer = vlc.MediaPlayer()
current_files = os.listdir()
selection = 0
font: pygame.font.Font
screen: pygame.Surface
input_buffer = ""
starting_point = 0
font_size = 40


def search_string(text: str, pattern: str) -> bool:
    text_index = 0
    for pchar in pattern:
        matched = False
        for tchar in text[text_index:]:
            text_index += 1
            if pchar == tchar:
                matched = True
                break
        if not matched:
            return False
    return True


def parent_dir():
    global current_files
    global input_buffer
    global selection

    os.chdir('../')
    current_files = os.listdir()
    input_buffer = ""
    selection = 0


def open_file(index: int):
    global current_files
    global input_buffer
    global selection

    if len(current_files) == 0:
        return

    next_path = current_files[index]
    if os.path.isdir(next_path):
        os.chdir(next_path)
        current_files = os.listdir()
        input_buffer = ""
        selection = 0
    else:
        player.set_mrl(next_path)
        player.play()


def up():
    global selection

    selection -= 1
    selection = numpy.clip(selection, 0, len(current_files) - 1)


def down():
    global selection

    selection += 1
    selection = numpy.clip(selection, 0, len(current_files) - 1)


def on_key_down(key: int, mod: int, unicode: str):
    global selection
    global input_buffer

    if mod & pygame.KMOD_CTRL:
        pass
    else:
        match key:
            case pygame.K_ESCAPE:
                parent_dir()
            case pygame.K_RETURN:
                open_file(selection)
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
                input_buffer += unicode
                selection = 0


def on_mouse_button_down(button: int):
    global selection
    global font_size
    global font

    match button:
        case pygame.BUTTON_LEFT:
            x, y = pygame.mouse.get_pos()
            selection = int(y / font_size - starting_point - 1)
            selection = numpy.clip(selection, 0, len(current_files) - 1)
        case pygame.BUTTON_RIGHT:
            open_file(selection)
        case pygame.BUTTON_WHEELDOWN:
            if pygame.key.get_mods() & pygame.KMOD_CTRL:
                font_size -= 2
                font_size = numpy.clip(font_size, 20, 100)
                font = pygame.font.SysFont(None, font_size)
            else:
                down()
        case pygame.BUTTON_WHEELUP:
            if pygame.key.get_mods() & pygame.KMOD_CTRL:
                font_size += 2
                font_size = numpy.clip(font_size, 20, 100)
                font = pygame.font.SysFont(None, font_size)
            else:
                up()
        case pygame.BUTTON_MIDDLE:
            parent_dir()
        case pygame.BUTTON_X1:
            player.pause()
        case pygame.BUTTON_X2:
            player.play()


def render_text(text: str, position, color=(255, 255, 255)):
    font_image = font.render(text, True, color)
    screen.blit(font_image, position)


def main():
    global current_files
    global selection
    global font
    global screen
    global input_buffer
    global starting_point

    running = True
    player.audio_set_volume(100)

    pygame.init()
    screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
    pygame.display.set_caption("Search Player")
    font = pygame.font.SysFont(None, font_size)

    while running:
        event = pygame.event.wait()

        if event.type == pygame.QUIT:
            running = False
        match event.type:
            case pygame.QUIT:
                running = False
            case pygame.KEYDOWN:
                on_key_down(event.key, event.mod, event.unicode)
            case pygame.MOUSEBUTTONDOWN:
                on_mouse_button_down(event.button)

        current_files = []
        for file in os.listdir():
            if search_string(file.lower(), input_buffer.lower()):
                current_files.append(file)

        screen.fill((30, 30, 30))

        starting_point = 0
        if selection >= (screen.get_height() / font_size) / 2:
            starting_point = -selection + (screen.get_height() / font_size) / 2 - 1
        
        pygame.draw.rect(screen, (225, 30, 30), (0, (selection + 1 + starting_point) * font_size, screen.get_width(), font_size))
        for i, filename in enumerate(current_files):
            render_text(filename, (0, (i + 1 + starting_point) * font_size))

        pygame.draw.rect(screen, (30, 30, 225), (0, 0, screen.get_width(), font_size))
        render_text(input_buffer, (0, 0))

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()