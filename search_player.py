import vlc
import os
import pygame
import numpy
import enum


class Mode(enum.Enum):
    DIR = 1
    COMMAND = 2
    ERROR = 3


def list_directory() -> list[str]:
    retval = os.listdir()
    retval.append(".")
    retval.append("..")
    
    for i, file in enumerate(retval):
        if os.path.isdir(file):
            retval[i] += "/"

    return retval


player: vlc.MediaPlayer = vlc.MediaPlayer()
current_files = list_directory()
selection = 0
font: pygame.font.Font
screen: pygame.Surface
filename_buffer = ""
command_buffer = ""
starting_point = 0
font_size = 40
mode = Mode.DIR
error_message = ""


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
    global filename_buffer
    global selection

    os.chdir('../')
    current_files = list_directory()
    filename_buffer = ""
    selection = 0


def open_file(index: int):
    global current_files
    global filename_buffer
    global selection

    if len(current_files) == 0:
        return

    next_path = current_files[index]
    if os.path.isdir(next_path):
        os.chdir(next_path)
        current_files = list_directory()
        filename_buffer = ""
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


def render_text(text: str, position, color=(255, 255, 255)):
    font_image = font.render(text, True, color)
    screen.blit(font_image, position)


def render_dir():
    pygame.draw.rect(screen, (225, 30, 30), (0, (selection + 1 + starting_point) * font_size, screen.get_width(), font_size))
    for i, filename in enumerate(current_files):
        if os.path.isdir(filename):
            render_text(filename, (0, (i + 1 + starting_point) * font_size), color=(255, 255, 0))
        else:
            render_text(filename, (0, (i + 1 + starting_point) * font_size))


def render_filename_buffer():
    pygame.draw.rect(screen, (30, 30, 225), (0, 0, screen.get_width(), font_size))
    render_text(filename_buffer, (0, 0))


def render_command_buffer():
    pygame.draw.rect(screen, (30, 255, 30), (0, 0, screen.get_width(), font_size))
    render_text(command_buffer, (0, 0))


def render_error():
    render_text(error_message, (0, 0))


def exe_cmd(cmd: list[str]):
    if len(cmd) == 0:
        raise Exception("Nothing to execute")
    match cmd[0].lower():
        case "open" | "o":
            match len(cmd):
                case 1:
                    open_file(selection)
                case 2:
                    try:
                        open_file(int(cmd[1]))
                    except:
                        raise Exception(f"\"{cmd[1]}\" was expected as integer")
                case _:
                    raise Exception("Too many arguments")
        case "stop":
            player.stop()
        case "play" | "s":
            player.play()
        case "pause" | "p":
            player.set_pause(1)
        case _:
            raise Exception(f"There is no command named \"{cmd[0]}\"")


def tokenize(raw_cmd: str) -> list[str]:
    return raw_cmd.split()


def on_key_down(key: int, mod: int, unicode: str):
    global selection
    global filename_buffer
    global mode
    global command_buffer
    global error_message

    match mode:
        case Mode.DIR:
            if mod & pygame.KMOD_CTRL:
                match key:
                    case pygame.K_c:
                        mode = Mode.COMMAND
                    case pygame.K_d:
                        filename_buffer = ""
                    case pygame.K_p:
                        parent_dir()
                    case pygame.K_s:
                        player.play()
                    case pygame.K_q:
                        player.set_pause(1)
            else:
                match key:
                    case pygame.K_ESCAPE:
                        pass
                    case pygame.K_RETURN | pygame.K_RIGHT:
                        open_file(selection)
                    case pygame.K_UP:
                        up()
                    case pygame.K_DOWN:
                        down()
                    case pygame.K_LEFT:
                        parent_dir()
                    case pygame.K_BACKSPACE:
                        filename_buffer = filename_buffer[:-1]
                        selection = 0
                    case _:
                        filename_buffer += unicode
                        selection = 0
        case Mode.COMMAND:
            if mod & pygame.KMOD_CTRL:
                match key:
                    case pygame.K_d:
                        command_buffer = ""
            else:
                match key:
                    case pygame.K_ESCAPE:
                        mode = Mode.DIR
                    case pygame.K_RETURN:
                        try:
                            exe_cmd(tokenize(command_buffer))
                        except(Exception) as e:
                            error_message = str(e)
                            mode = Mode.ERROR
                    case pygame.K_BACKSPACE:
                        command_buffer = command_buffer[:-1]
                    case _:
                        command_buffer += unicode
        case Mode.ERROR:
            mode = Mode.DIR
            error_message = ""


def on_mouse_button_down(button: int):
    global selection
    global font_size
    global font

    match mode:
        case Mode.DIR:
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
                    player.pause()
                case pygame.BUTTON_X1:
                    parent_dir()
                case pygame.BUTTON_X2:
                    open_file(selection)



def main():
    global current_files
    global selection
    global font
    global screen
    global filename_buffer
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
        for file in list_directory():
            if search_string(file.lower(), filename_buffer.lower()):
                current_files.append(file)

        starting_point = 0
        if selection >= (screen.get_height() / font_size) / 2:
            starting_point = -selection + (screen.get_height() / font_size) / 2 - 1

        screen.fill((30, 30, 30))

        match mode:
            case Mode.DIR:
                render_dir()
                render_filename_buffer()
            case Mode.COMMAND:
                render_dir()
                render_command_buffer()
            case Mode.ERROR:
                render_error()

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()