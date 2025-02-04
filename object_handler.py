from sprite_object import *
from npc import *
from random import choices, randrange


class ObjectHandler:
    def __init__(self, game):
        self.game = game
        self.sprite_list = []  # Lista de sprites estáticos e animados
        self.npc_list = []  # Lista de NPCs ativos no jogo
        self.npc_sprite_path = 'resources/sprites/npc/'
        self.static_sprite_path = 'resources/sprites/static_sprites/'
        self.anim_sprite_path = 'resources/sprites/animated_sprites/'
        self.npc_positions = {}  # Dicionário para armazenar posições dos NPCs no mapa
        
        add_sprite = self.add_sprite
        add_npc = self.add_npc

        # Configuração de NPCs
        self.enemies = 20  # Número de NPCs no jogo
        self.npc_types = [SoldierNPC, CacoDemonNPC, CyberDemonNPC]  # Tipos de NPCs disponíveis
        self.weights = [70, 20, 10]  # Probabilidades de spawn para cada tipo
        self.restricted_area = {(i, j) for i in range(10) for j in range(10)}  # Área onde NPCs não podem spawnar
        self.spawn_npc()

        # Adicionando sprites ao mapa
        add_sprite(AnimatedSprite(game))
        add_sprite(AnimatedSprite(game, pos=(1.5, 1.5)))
        add_sprite(AnimatedSprite(game, pos=(1.5, 7.5)))
        add_sprite(AnimatedSprite(game, pos=(5.5, 3.25)))
        add_sprite(AnimatedSprite(game, pos=(5.5, 4.75)))
        add_sprite(AnimatedSprite(game, pos=(7.5, 2.5)))
        add_sprite(AnimatedSprite(game, pos=(7.5, 5.5)))
        add_sprite(AnimatedSprite(game, pos=(14.5, 1.5)))
        add_sprite(AnimatedSprite(game, pos=(14.5, 4.5)))
        add_sprite(AnimatedSprite(game, path=self.anim_sprite_path + 'red_light/0.png', pos=(14.5, 5.5)))
        add_sprite(AnimatedSprite(game, path=self.anim_sprite_path + 'red_light/0.png', pos=(14.5, 7.5)))
        add_sprite(AnimatedSprite(game, path=self.anim_sprite_path + 'red_light/0.png', pos=(12.5, 7.5)))
        add_sprite(AnimatedSprite(game, path=self.anim_sprite_path + 'red_light/0.png', pos=(9.5, 7.5)))
        add_sprite(AnimatedSprite(game, path=self.anim_sprite_path + 'red_light/0.png', pos=(14.5, 12.5)))
        add_sprite(AnimatedSprite(game, path=self.anim_sprite_path + 'red_light/0.png', pos=(9.5, 20.5)))
        add_sprite(AnimatedSprite(game, path=self.anim_sprite_path + 'red_light/0.png', pos=(10.5, 20.5)))
        add_sprite(AnimatedSprite(game, path=self.anim_sprite_path + 'red_light/0.png', pos=(3.5, 14.5)))
        add_sprite(AnimatedSprite(game, path=self.anim_sprite_path + 'red_light/0.png', pos=(3.5, 18.5)))
        add_sprite(AnimatedSprite(game, pos=(14.5, 24.5)))
        add_sprite(AnimatedSprite(game, pos=(14.5, 30.5)))
        add_sprite(AnimatedSprite(game, pos=(1.5, 30.5)))
        add_sprite(AnimatedSprite(game, pos=(1.5, 24.5)))

    def spawn_npc(self):
        """ Spawna NPCs aleatoriamente no mapa, evitando áreas restritas e paredes """
        for _ in range(self.enemies):
            npc = choices(self.npc_types, self.weights)[0]  # Escolhe um tipo de NPC com base nas probabilidades
            pos = x, y = randrange(self.game.map.cols), randrange(self.game.map.rows)

            # Garante que o NPC não spawne em uma parede ou área restrita
            while (pos in self.game.map.world_map) or (pos in self.restricted_area):
                pos = x, y = randrange(self.game.map.cols), randrange(self.game.map.rows)

            self.add_npc(npc(self.game, pos=(x + 0.5, y + 0.5)))

    def check_win(self):
        """ Verifica se todos os NPCs foram eliminados para declarar vitória """
        if not len(self.npc_positions):
            self.game.object_renderer.win()
            pg.display.flip()
            pg.time.delay(1500)
            self.game.new_game()

    def update(self):
        """ Atualiza a posição dos NPCs e sprites a cada frame """
        self.npc_positions = {npc.map_pos for npc in self.npc_list if npc.alive}
        [sprite.update() for sprite in self.sprite_list]
        [npc.update() for npc in self.npc_list]
        self.check_win()

    def add_npc(self, npc):
        """ Adiciona um NPC à lista de NPCs ativos """
        self.npc_list.append(npc)

    def add_sprite(self, sprite):
        """ Adiciona um sprite à lista de sprites ativos """
        self.sprite_list.append(sprite)
