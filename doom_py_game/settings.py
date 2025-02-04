import math

# Configurações principais do jogo

# Resolução da tela (largura e altura)
RES = WIDTH, HEIGHT = 1366, 768

# Metade da largura e altura, usadas para cálculos de perspectiva
HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2

# Taxa de quadros por segundo (FPS)
FPS = 0  # Pode ser ajustado conforme necessário

# Configurações do jogador
PLAYER_POS = 1.5, 5  # Posição inicial do jogador no mapa (coordenadas no grid)
PLAYER_ANGLE = 0  # Ângulo inicial de visão do jogador (0 = olhando para a direita)
PLAYER_SPEED = 0.004  # Velocidade de movimento do jogador
PLAYER_ROT_SPEED = 0.002  # Velocidade de rotação do jogador
PLAYER_SIZE_SCALE = 60  # Escala do tamanho do jogador para colisões
PLAYER_MAX_HEALTH = 100  # Vida máxima do jogador

# Configurações do mouse
MOUSE_SENSITIVITY = 0.0003  # Sensibilidade do mouse para girar a câmera
MOUSE_MAX_REL = 40  # Movimento máximo permitido do mouse antes de ser resetado
MOUSE_BORDER_LEFT = 100  # Margem esquerda para resetar a posição do mouse
MOUSE_BORDER_RIGHT = WIDTH - MOUSE_BORDER_LEFT  # Margem direita para resetar a posição do mouse

# Cor do chão no jogo (RGB)
FLOOR_COLOR = (30, 30, 30)

# Configurações do campo de visão (FOV - Field of View)
FOV = math.pi / 3  # Campo de visão do jogador (60°)
HALF_FOV = FOV / 2  # Metade do FOV (usado para cálculos)
NUM_RAYS = WIDTH // 2  # Número de raios lançados para o raycasting
HALF_NUM_RAYS = NUM_RAYS // 2  # Metade do número de raios (usado para cálculos)
DELTA_ANGLE = FOV / NUM_RAYS  # Diferença de ângulo entre cada raio lançado
MAX_DEPTH = 20  # Distância máxima de visão

# Distância da tela para projeção 3D (evita distorções visuais)
SCREEN_DIST = HALF_WIDTH / math.tan(HALF_FOV)

# Escala dos raios (usado para renderização das paredes)
SCALE = WIDTH // NUM_RAYS

# Configurações de texturas
TEXTURE_SIZE = 256  # Tamanho das texturas quadradas (256x256 pixels)
HALF_TEXTURE_SIZE = TEXTURE_SIZE // 2  # Metade do tamanho da textura (128 pixels)
