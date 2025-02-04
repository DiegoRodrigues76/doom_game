import pygame as pg


class Sound:
    def __init__(self, game):
        self.game = game  # Referência ao jogo

        # Inicializa o mixer de áudio do Pygame
        pg.mixer.init()

        # Caminho para a pasta de sons
        self.path = 'resources/sound/'

        # Carrega os efeitos sonoros
        self.shotgun = pg.mixer.Sound(self.path + 'shotgun.wav')  # Som de tiro
        self.npc_pain = pg.mixer.Sound(self.path + 'npc_pain.wav')  # Som de dor do NPC
        self.npc_death = pg.mixer.Sound(self.path + 'npc_death.wav')  # Som de morte do NPC
        self.npc_shot = pg.mixer.Sound(self.path + 'npc_attack.wav')  # Som de tiro do NPC
        self.npc_shot.set_volume(0.2)  # Define o volume do tiro do NPC para 20%
        
        self.player_pain = pg.mixer.Sound(self.path + 'player_pain.wav')  # Som de dano no jogador

        # Carrega a música de fundo
        self.theme = pg.mixer.music.load(self.path + 'theme.mp3')
        pg.mixer.music.set_volume(0.3)  # Define o volume da música para 30%
