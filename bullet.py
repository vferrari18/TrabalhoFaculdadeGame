import pygame
import math


class Bala(pygame.sprite.Sprite):
    # --- NOVO: O Molde da Bala ---
    molde_imagem = None

    def __init__(self, x, y, destino_x, destino_y):
        super().__init__()

        # Se o molde da bala não existe ainda, cria ele na memória de vídeo
        if Bala.molde_imagem is None:
            Bala.molde_imagem = pygame.Surface((10, 5)).convert()
            Bala.molde_imagem.fill((255, 255, 0))

            # Pega a imagem pronta sem gastar processamento
        self.image = Bala.molde_imagem

        self.rect = self.image.get_rect(center=(x, y))
        self.dano = 30

        # Matemática para mirar
        angulo = math.atan2(destino_y - y, destino_x - x)
        self.vx = math.cos(angulo) * 15
        self.vy = math.sin(angulo) * 15

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy

        # Destrói a bala se sair da tela (mantendo a memória limpa)
        if self.rect.right < 0 or self.rect.left > 800 or self.rect.bottom < 0 or self.rect.top > 600:
            self.kill()