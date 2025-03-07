#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame.key
from code.Const import ENTITY_SPEED, WIN_HEIGHT, WIN_WIDTH, PLAYER_KEY_UP, PLAYER_KEY_DOWN, PLAYER_KEY_LEFT, \
    PLAYER_KEY_RIGHT, PLAYER_KEY_SHOOT, ENTITY_SHOT_DELAY
from code.Entity import Entity
from code.PlayerShot import PlayerShot

class Player(Entity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)
        self.shot_delay = ENTITY_SHOT_DELAY[self.name]

    def move(self):
        pressed_key = pygame.key.get_pressed()  # Obtém os estados das teclas pressionadas de uma vez

        # Dicionário que mapeia a direção para a chave correspondente
        movement_keys = {
            'up': (PLAYER_KEY_UP[self.name], 0, -ENTITY_SPEED[self.name]),
            'down': (PLAYER_KEY_DOWN[self.name], 0, ENTITY_SPEED[self.name]),
            'left': (PLAYER_KEY_LEFT[self.name], -ENTITY_SPEED[self.name], 0),
            'right': (PLAYER_KEY_RIGHT[self.name], ENTITY_SPEED[self.name], 0)
        }

        for direction, (key, dx, dy) in movement_keys.items():
            if pressed_key[key]:
                # Checa se o movimento está dentro dos limites da janela
                if direction == 'up' and self.rect.top > 0 or \
                   direction == 'down' and self.rect.bottom < WIN_HEIGHT or \
                   direction == 'left' and self.rect.left > 0 or \
                   direction == 'right' and self.rect.right < WIN_WIDTH:
                    self.rect.move_ip(dx, dy)

    def shoot(self):
        self.shot_delay -= 1  # Diminui o tempo de delay para o próximo tiro
        if self.shot_delay <= 0:
            self.shot_delay = ENTITY_SHOT_DELAY[self.name]  # Reseta o delay do tiro
            pressed_key = pygame.key.get_pressed()
            # Checa se a tecla de atirar foi pressionada
            if pressed_key[PLAYER_KEY_SHOOT[self.name]]:
                return PlayerShot(name=f'{self.name}Shot', position=(self.rect.centerx, self.rect.centery))
        return None  # Se não atirar, retorna None
