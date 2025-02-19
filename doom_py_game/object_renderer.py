import pygame as pg
from settings import *


class ObjectRenderer:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        
        # Carrega as texturas das paredes
        self.wall_textures = self.load_wall_textures()
        
        # Carrega a textura do céu e define o deslocamento inicial
        self.sky_image = self.get_texture('resources/textures/sky.png', (WIDTH, HALF_HEIGHT))
        self.sky_offset = 0

        # Efeito de dano na tela
        self.blood_screen = self.get_texture('resources/textures/blood_screen.png', RES)
        
        # Carrega as imagens dos números para exibir a vida do jogador
        self.digit_size = 90
        self.digit_images = [self.get_texture(f'resources/textures/digits/{i}.png', [self.digit_size] * 2)
                             for i in range(11)]
        self.digits = dict(zip(map(str, range(11)), self.digit_images))
        
        # Carrega as telas de "Game Over" e "Vitória"
        self.game_over_image = self.get_texture('resources/textures/game_over.png', RES)
        self.win_image = self.get_texture('resources/textures/win.png', RES)

    def draw(self):
        """Desenha o fundo, os objetos do jogo e a interface do jogador."""
        self.draw_background()
        self.render_game_objects()
        self.draw_player_health()

    def win(self):
        """Exibe a tela de vitória."""
        self.screen.blit(self.win_image, (0, 0))

    def game_over(self):
        """Exibe a tela de game over."""
        self.screen.blit(self.game_over_image, (0, 0))

    def draw_player_health(self):
        """Exibe a vida do jogador no canto da tela."""
        health = str(self.game.player.health)
        for i, char in enumerate(health):
            self.screen.blit(self.digits[char], (i * self.digit_size, 0))
        self.screen.blit(self.digits['10'], ((i + 1) * self.digit_size, 0))  # Exibe "/10" ao lado da vida

    def player_damage(self):
        """Mostra um efeito de dano na tela quando o jogador recebe dano."""
        self.screen.blit(self.blood_screen, (0, 0))

    def draw_background(self):
        """Desenha o céu e o chão do jogo."""
        # Movimentação do céu baseada no movimento do mouse
        self.sky_offset = (self.sky_offset + 4.5 * self.game.player.rel) % WIDTH
        self.screen.blit(self.sky_image, (-self.sky_offset, 0))
        self.screen.blit(self.sky_image, (-self.sky_offset + WIDTH, 0))
        
        # Desenha o chão com uma cor fixa
        pg.draw.rect(self.screen, FLOOR_COLOR, (0, HALF_HEIGHT, WIDTH, HEIGHT))

    def render_game_objects(self):
        """Renderiza os objetos do jogo na tela, priorizando os mais próximos."""
        list_objects = sorted(self.game.raycasting.objects_to_render, key=lambda t: t[0], reverse=True)
        for depth, image, pos in list_objects:
            self.screen.blit(image, pos)

    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        """Carrega uma textura da imagem especificada e a redimensiona."""
        texture = pg.image.load(path).convert_alpha()
        return pg.transform.scale(texture, res)

    def load_wall_textures(self):
        """Carrega e retorna as texturas das paredes do jogo."""
        return {
            1: self.get_texture('resources/textures/1.png'),
            2: self.get_texture('resources/textures/2.png'),
            3: self.get_texture('resources/textures/3.png'),
            4: self.get_texture('resources/textures/4.png'),
            5: self.get_texture('resources/textures/5.png'),
        }
