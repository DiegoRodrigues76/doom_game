import pygame as pg
import math
from settings import *


class RayCasting:
    def __init__(self, game):
        self.game = game
        self.ray_casting_result = []  # Armazena os resultados do raycasting
        self.objects_to_render = []  # Lista de objetos a serem renderizados na tela
        self.textures = self.game.object_renderer.wall_textures  # Carrega as texturas das paredes

    def get_objects_to_render(self):
        """
        Processa os resultados do raycasting e gera as colunas de parede
        com a altura correta para simular a perspectiva.
        """
        self.objects_to_render = []

        for ray, values in enumerate(self.ray_casting_result):
            depth, proj_height, texture, offset = values

            if proj_height < HEIGHT:
                # Se a projeção da parede cabe na tela normalmente
                wall_column = self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - SCALE), 0, SCALE, TEXTURE_SIZE
                )
                wall_column = pg.transform.scale(wall_column, (SCALE, proj_height))
                wall_pos = (ray * SCALE, HALF_HEIGHT - proj_height // 2)
            else:
                # Se a projeção da parede ultrapassa a altura da tela (ajuste da textura)
                texture_height = TEXTURE_SIZE * HEIGHT / proj_height
                wall_column = self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - SCALE), HALF_TEXTURE_SIZE - texture_height // 2,
                    SCALE, texture_height
                )
                wall_column = pg.transform.scale(wall_column, (SCALE, HEIGHT))
                wall_pos = (ray * SCALE, 0)

            self.objects_to_render.append((depth, wall_column, wall_pos))

    def ray_cast(self):
        """
        Implementa o algoritmo de raycasting, simulando raios projetados a partir da visão do jogador
        para detectar paredes e calcular a profundidade dos objetos na cena.
        """
        self.ray_casting_result = []
        texture_vert, texture_hor = 1, 1  # Variáveis para armazenar texturas das interseções
        ox, oy = self.game.player.pos  # Posição do jogador
        x_map, y_map = self.game.player.map_pos  # Posição do jogador no mapa (grid)

        ray_angle = self.game.player.angle - HALF_FOV + 0.0001  # Primeiro ângulo do raio

        for ray in range(NUM_RAYS):
            sin_a = math.sin(ray_angle)
            cos_a = math.cos(ray_angle)

            # *** Cálculo da interseção com linhas horizontais ***
            y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)
            depth_hor = (y_hor - oy) / sin_a
            x_hor = ox + depth_hor * cos_a

            delta_depth = dy / sin_a
            dx = delta_depth * cos_a

            for _ in range(MAX_DEPTH):
                tile_hor = int(x_hor), int(y_hor)
                if tile_hor in self.game.map.world_map:
                    texture_hor = self.game.map.world_map[tile_hor]
                    break
                x_hor += dx
                y_hor += dy
                depth_hor += delta_depth

            # *** Cálculo da interseção com linhas verticais ***
            x_vert, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, -1)
            depth_vert = (x_vert - ox) / cos_a
            y_vert = oy + depth_vert * sin_a

            delta_depth = dx / cos_a
            dy = delta_depth * sin_a

            for _ in range(MAX_DEPTH):
                tile_vert = int(x_vert), int(y_vert)
                if tile_vert in self.game.map.world_map:
                    texture_vert = self.game.map.world_map[tile_vert]
                    break
                x_vert += dx
                y_vert += dy
                depth_vert += delta_depth

            # Escolhe a interseção mais próxima (horizontal ou vertical)
            if depth_vert < depth_hor:
                depth, texture = depth_vert, texture_vert
                y_vert %= 1
                offset = y_vert if cos_a > 0 else (1 - y_vert)
            else:
                depth, texture = depth_hor, texture_hor
                x_hor %= 1
                offset = (1 - x_hor) if sin_a > 0 else x_hor

            # Correção do efeito "Fishbowl" (distância da projeção)
            depth *= math.cos(self.game.player.angle - ray_angle)

            # Cálculo da altura da parede com base na profundidade
            proj_height = SCREEN_DIST / (depth + 0.0001)

            # Armazena os resultados do raycasting
            self.ray_casting_result.append((depth, proj_height, texture, offset))

            # Incrementa o ângulo do próximo raio
            ray_angle += DELTA_ANGLE

    def update(self):
        """
        Atualiza o sistema de raycasting, recalculando os raios e preparando os objetos para renderização.
        """
        self.ray_cast()
        self.get_objects_to_render()
