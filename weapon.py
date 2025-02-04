from sprite_object import *

# Classe que representa a arma do jogador (herda de AnimatedSprite)
class Weapon(AnimatedSprite):
    def __init__(self, game, path='resources/sprites/weapon/shotgun/0.png', scale=0.4, animation_time=90):
        # Chama o construtor da classe base (AnimatedSprite)
        super().__init__(game=game, path=path, scale=scale, animation_time=animation_time)
        # Redimensiona as imagens de animação de acordo com a escala fornecida
        self.images = deque(
            [pg.transform.smoothscale(img, (self.image.get_width() * scale, self.image.get_height() * scale))
             for img in self.images])  
        # Define a posição da arma na tela (centralizada na parte inferior)
        self.weapon_pos = (HALF_WIDTH - self.images[0].get_width() // 2, HEIGHT - self.images[0].get_height())
        self.reloading = False  # Indica se a arma está recarregando
        self.num_images = len(self.images)  # Número de imagens na animação
        self.frame_counter = 0  # Contador de quadros de animação
        self.damage = 50  # Dano da arma

    # Função que controla a animação de disparo da arma
    def animate_shot(self):
        if self.reloading:  # Se a arma está recarregando
            self.game.player.shot = False  # Impede o jogador de disparar enquanto recarrega
            if self.animation_trigger:  # Se o tempo de animação passou
                self.images.rotate(-1)  # Avança para o próximo quadro na animação
                self.image = self.images[0]  # Atualiza a imagem exibida
                self.frame_counter += 1  # Aumenta o contador de quadros
                if self.frame_counter == self.num_images:  # Se todos os quadros foram exibidos
                    self.reloading = False  # A arma terminou de recarregar
                    self.frame_counter = 0  # Reseta o contador de quadros

    # Função para desenhar a arma na tela
    def draw(self):
        self.game.screen.blit(self.images[0], self.weapon_pos)  # Desenha a primeira imagem da animação

    # Função chamada a cada atualização do jogo
    def update(self):
        self.check_animation_time()  # Verifica o tempo da animação
        self.animate_shot()  # Controla a animação do disparo (ou recarga)
