#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import pygame

from code.Const import WIN_WIDTH, WIN_HEIGHT, MENU_OPTION
from code.Level import Level
from code.Menu import Menu
from code.Score import Score


class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode(size=(WIN_WIDTH, WIN_HEIGHT))
        self.running = True

    def start_game(self, menu_return):
        player_score = [0, 0]  # [Jogador1, Jogador2]
        for level_name in ['Level1', 'Level2']:
            level = Level(self.window, level_name, menu_return, player_score)
            if not level.run(player_score):
                return
        Score(self.window).save(menu_return, player_score)

    def run(self):
        while self.running:
            menu = Menu(self.window)
            menu_return = menu.run()

            if menu_return in MENU_OPTION[:3]:  # Se for uma opção de jogo
                self.start_game(menu_return)
            elif menu_return == MENU_OPTION[3]:  # Exibir pontuações
                Score(self.window).show()
            elif menu_return == MENU_OPTION[4]:  # Sair
                self.quit_game()

    def quit_game(self):
        pygame.quit()
        sys.exit()
