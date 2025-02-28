from typing import Any

import pygame

from code.Const import WIN_HEIGHT, WIN_WIDTH, MENU_OPTION
from code.menu import Menu


class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode(size=(WIN_WIDTH, WIN_HEIGHT))

    def run(self):
        while True:
            menu = Menu(self.window)
            menu_return = menu.run()

            if menu_return == MENU_OPTION[0]:
                pass
            elif menu_return == MENU_OPTION[2]:
                pygame.quit()
                quit()
            else:
                pass


