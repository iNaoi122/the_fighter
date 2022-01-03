import pygame_menu
import pygame

from Fighter import game_cycle

pygame.init()
screen = pygame.display.set_mode((600, 600))

menu = pygame_menu.Menu("Fighter", 400, 300, theme=pygame_menu.themes.THEME_DEFAULT)

menu.add.button("Play", game_cycle)
menu.add.button('Quit', pygame_menu.events.EXIT)

menu.mainloop(screen)
