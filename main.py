import pygame as pg
import sys
from settings import *
from map import *
from player import *
from raycasting import *
from object_renderer import *
from sprite_object import *
from object_handler import *
from weapon import *
from sound import *
from pathfinding import *

class Game:
    def __init__(self):
        pg.init()
        pg.mouse.set_visible(False)
        self.screen = pg.display.set_mode(RES)
        pg.event.set_grab(True)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.global_trigger = False
        self.global_event = pg.USEREVENT + 0
        pg.time.set_timer(self.global_event, 40)  # Define um evento global que ocorre a cada 40ms
        self.new_game()

    def new_game(self):
        """Inicializa os componentes do jogo."""
        self.map = Map(self)
        self.player = Player(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self)
        self.object_handler = ObjectHandler(self)
        self.weapon = Weapon(self)
        self.sound = Sound(self)
        self.pathfinding = PathFinding(self)
        pg.mixer.music.play(-1)  # Inicia a música de fundo em loop

    def update(self):
        """Atualiza os elementos do jogo e controla o FPS."""
        self.player.update()
        self.raycasting.update()
        self.object_handler.update()
        self.weapon.update()
        pg.display.flip()  # Atualiza a tela
        self.delta_time = self.clock.tick(FPS)  # Mantém o jogo na taxa de quadros definida
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')  # Exibe o FPS na janela

    def draw(self):
        """Renderiza os elementos visuais."""
        self.object_renderer.draw()
        self.weapon.draw()

    def check_events(self):
        """Verifica os eventos do jogo, como entrada do jogador e saída."""
        self.global_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif event.type == self.global_event:
                self.global_trigger = True
            self.player.single_fire_event(event)

    def run(self):
        """Loop principal do jogo."""
        while True:
            self.check_events()
            self.update()
            self.draw()

if __name__ == '__main__':
    game = Game()
    game.run()
