import pygame as pg
from settings import *
import os
from collections import deque

# Classe para objetos estáticos no jogo (ex. uma vela)
class SpriteObject:
    def __init__(self, game, path='resources/sprites/static_sprites/candlebra.png',
                 pos=(10.5, 3.5), scale=0.7, shift=0.27):
        self.game = game
        self.player = game.player
        self.x, self.y = pos
        self.image = pg.image.load(path).convert_alpha()  # Carrega a imagem do sprite
        self.IMAGE_WIDTH = self.image.get_width()  # Largura da imagem
        self.IMAGE_HALF_WIDTH = self.image.get_width() // 2  # Metade da largura
        self.IMAGE_RATIO = self.IMAGE_WIDTH / self.image.get_height()  # Proporção largura/altura
        self.dx, self.dy, self.theta, self.screen_x, self.dist, self.norm_dist = 0, 0, 0, 0, 1, 1
        self.sprite_half_width = 0
        self.SPRITE_SCALE = scale  # Fator de escala do sprite
        self.SPRITE_HEIGHT_SHIFT = shift  # Deslocamento na altura do sprite

    # Função para calcular a projeção do sprite na tela
    def get_sprite_projection(self):
        proj = SCREEN_DIST / self.norm_dist * self.SPRITE_SCALE  # Projeção do sprite
        proj_width, proj_height = proj * self.IMAGE_RATIO, proj  # Largura e altura projetadas

        image = pg.transform.scale(self.image, (proj_width, proj_height))  # Redimensiona o sprite

        self.sprite_half_width = proj_width // 2  # Metade da largura projetada
        height_shift = proj_height * self.SPRITE_HEIGHT_SHIFT  # Deslocamento na altura
        pos = self.screen_x - self.sprite_half_width, HALF_HEIGHT - proj_height // 2 + height_shift  # Posição final na tela

        # Adiciona o sprite projetado à lista de objetos a renderizar
        self.game.raycasting.objects_to_render.append((self.norm_dist, image, pos))

    # Função para calcular os dados necessários para o sprite
    def get_sprite(self):
        dx = self.x - self.player.x  # Distância horizontal
        dy = self.y - self.player.y  # Distância vertical
        self.dx, self.dy = dx, dy
        self.theta = math.atan2(dy, dx)  # Calcula o ângulo do sprite

        delta = self.theta - self.player.angle  # Diferença entre os ângulos
        if (dx > 0 and self.player.angle > math.pi) or (dx < 0 and dy < 0):
            delta += math.tau  # Ajuste para o ângulo
        delta_rays = delta / DELTA_ANGLE  # Cálculo da distância em raios
        self.screen_x = (HALF_NUM_RAYS + delta_rays) * SCALE  # Posição na tela

        self.dist = math.hypot(dx, dy)  # Distância até o sprite
        self.norm_dist = self.dist * math.cos(delta)  # Distância normalizada
        # Verifica se o sprite está na tela e se é visível
        if -self.IMAGE_HALF_WIDTH < self.screen_x < (WIDTH + self.IMAGE_HALF_WIDTH) and self.norm_dist > 0.5:
            self.get_sprite_projection()

    # Função que é chamada a cada atualização
    def update(self):
        self.get_sprite()

# Classe para objetos com animação
class AnimatedSprite(SpriteObject):
    def __init__(self, game, path='resources/sprites/animated_sprites/green_light/0.png',
                 pos=(11.5, 3.5), scale=0.8, shift=0.16, animation_time=120):
        super().__init__(game, path, pos, scale, shift)  # Chama o construtor da classe base
        self.animation_time = animation_time  # Tempo de animação
        self.path = path.rsplit('/', 1)[0]  # Caminho da pasta de animação
        self.images = self.get_images(self.path)  # Lista de imagens da animação
        self.animation_time_prev = pg.time.get_ticks()  # Marca o tempo da última animação
        self.animation_trigger = False  # Controla quando a animação deve ser trocada

    # Função de atualização da animação
    def update(self):
        super().update()  # Chama o update da classe base
        self.check_animation_time()  # Verifica o tempo da animação
        self.animate(self.images)  # Executa a animação

    # Função para realizar a troca de imagens na animação
    def animate(self, images):
        if self.animation_trigger:  # Se o tempo de animação passou
            images.rotate(-1)  # Rotaciona as imagens
            self.image = images[0]  # Atualiza a imagem exibida

    # Verifica se o tempo da animação passou
    def check_animation_time(self):
        self.animation_trigger = False  # Reseta o gatilho
        time_now = pg.time.get_ticks()  # Pega o tempo atual
        if time_now - self.animation_time_prev > self.animation_time:  # Se passou o tempo de animação
            self.animation_time_prev = time_now  # Atualiza o tempo
            self.animation_trigger = True  # Gatilho para mudar a animação

    # Função para carregar todas as imagens da animação
    def get_images(self, path):
        images = deque()  # Usando deque para facilitar a rotação das imagens
        for file_name in os.listdir(path):  # Percorre todos os arquivos na pasta de animação
            if os.path.isfile(os.path.join(path, file_name)):  # Verifica se é um arquivo
                img = pg.image.load(path + '/' + file_name).convert_alpha()  # Carrega a imagem
                images.append(img)  # Adiciona na lista de imagens
        return images  # Retorna a lista de imagens
