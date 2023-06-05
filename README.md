# search-player

![Screenshot (279)](https://user-images.githubusercontent.com/92769408/232170267-8942584d-dd68-4e24-9acb-1a843a18d9ba.png)
![Screenshot (278)](https://user-images.githubusercontent.com/92769408/232170270-a68a05fa-0b85-49fd-b08a-b04774add538.png)
![Screenshot from 2023-04-15 08-52-36](https://user-images.githubusercontent.com/92769408/232171837-5772ca17-9144-48d8-9240-6e8d9397b17f.png)
Search Player is a file explorer that opens a file. It includes fast navigation and fast searching files.

# How to use
1.  Install Python3
2.  Install PIP3
3.  Run `pip3 install -r requirements.txt`
4.  Run `python3 search_player.py`

# Configuration
To get started, add a file named `~/.searchplayerconf.ini`.

The default configuration looks like this:
```
[fs]
initial_directory = /
[visual]
initial_fontsize = 40
font = None
theme = light
frame_thinness = 3
[key]
page_updown_speed = 8
```

Copy this and paste into `~/.searchplayerconf.ini`, and edit the values.

Also, you can print available fonts by this command
```
python3 -c "import pygame;print(pygame.font.get_fonts())"
```
