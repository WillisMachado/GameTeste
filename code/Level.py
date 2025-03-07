import random
import sys
import pygame
from pygame import Surface, Rect
from pygame.font import Font

from code.Const import C_WHITE, WIN_HEIGHT, MENU_OPTION, EVENT_ENEMY, SPAWN_TIME, C_ORANGE, C_CYAN, EVENT_TIMEOUT, \
    TIMEOUT_STEP, TIMEOUT_LEVEL
from code.Enemy import Enemy
from code.Entity import Entity
from code.EntityFactory import EntityFactory
from code.EntityMediator import EntityMediator
from code.Player import Player


class Level:
    def __init__(self, window: Surface, name: str, game_mode: str, player_score: list[int]):
        self.timeout = TIMEOUT_LEVEL
        self.window = window
        self.name = name
        self.game_mode = game_mode
        self.entity_list: list[Entity] = []
        self.entity_list.extend(EntityFactory.get_entity(self.name + 'Bg'))
        self.add_players(player_score)

        pygame.time.set_timer(EVENT_ENEMY, SPAWN_TIME)
        pygame.time.set_timer(EVENT_TIMEOUT, TIMEOUT_STEP)

    def add_players(self, player_score):
        player1 = EntityFactory.get_entity('Player1')
        player1.score = player_score[0]
        self.entity_list.append(player1)

        if self.game_mode in [MENU_OPTION[1], MENU_OPTION[2]]:
            player2 = EntityFactory.get_entity('Player2')
            player2.score = player_score[1]
            self.entity_list.append(player2)

    def run(self, player_score: list[int]):
        pygame.mixer_music.stop()  # Para qualquer música anterior
        pygame.mixer_music.load(f'./asset/{self.name}.mp3')  # Carrega a música do nível atual
        pygame.mixer_music.set_volume(0.3)
        pygame.mixer_music.play(-1)  # Começa a tocar em loop

        clock = pygame.time.Clock()

        while True:
            clock.tick(60)
            if self.handle_events(player_score):
                return True
            if not any(isinstance(ent, Player) for ent in self.entity_list):
                return False

            self.update_entities()
            self.draw_screen(clock)

    def handle_events(self, player_score):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == EVENT_ENEMY:
                choice = random.choice(('Enemy1', 'Enemy2'))
                self.entity_list.append(EntityFactory.get_entity(choice))
            elif event.type == EVENT_TIMEOUT:
                self.timeout -= TIMEOUT_STEP
                if self.timeout == 0:
                    self.update_scores(player_score)
                    return True
        return False

    def update_scores(self, player_score):
        for ent in self.entity_list:
            if isinstance(ent, Player):
                if ent.name == 'Player1':
                    player_score[0] = ent.score
                elif ent.name == 'Player2':
                    player_score[1] = ent.score

    def update_entities(self):
        for ent in self.entity_list:
            self.window.blit(source=ent.surf, dest=ent.rect)
            ent.move()
            if isinstance(ent, (Player, Enemy)):
                shoot = ent.shoot()
                if shoot:
                    self.entity_list.append(shoot)
        EntityMediator.verify_collision(entity_list=self.entity_list)
        EntityMediator.verify_health(entity_list=self.entity_list)

    def draw_screen(self, clock):
        for ent in self.entity_list:
            if isinstance(ent, Player):
                color = C_ORANGE if ent.name == 'Player1' else C_CYAN
                y_pos = 25 if ent.name == 'Player1' else 45
                self.level_text(18, f'{ent.name} - Health: {ent.health} | Score: {ent.score}', color, (10, y_pos))

        self.level_text(18, f'{self.name} - Timeout: {self.timeout / 1000:.1f}s', C_WHITE, (10, 5))
        self.level_text(18, f'fps: {clock.get_fps():.0f}', C_WHITE, (10, WIN_HEIGHT - 35))
        self.level_text(18, f'entidades: {len(self.entity_list)}', C_WHITE, (10, WIN_HEIGHT - 20))
        pygame.display.flip()

    def level_text(self, text_size: int, text: str, text_color: tuple, text_pos: tuple):
        text_font: Font = pygame.font.SysFont(name="Press Start 2P", size=text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(left=text_pos[0], top=text_pos[1])
        self.window.blit(source=text_surf, dest=text_rect)
