# search-player

![Screenshot (279)](https://user-images.githubusercontent.com/92769408/232170267-8942584d-dd68-4e24-9acb-1a843a18d9ba.png)
![Screenshot (278)](https://user-images.githubusercontent.com/92769408/232170270-a68a05fa-0b85-49fd-b08a-b04774add538.png)


# How to use
1.  Install Python3
2.  Install PIP3
3.  Run `pip3 install -r requirements.txt`
4.  Run `python3 search_player.py`

# Configuration
To get started, add a file named `~/.searchplayerconf`.

The default configuration looks like this:
```
initial_directory /
initial_fontsize 40
page_updown_speed 8
font None
theme light
frame_thinness 3
```

The grammar looks like this:
```
[key] [value]
```

Copy this and paste into `~/.searchplayerconf`, and edit the values.

Also, you can print available fonts by this command
```
python3 -c "import pygame;print(pygame.font.get_fonts())"
```
