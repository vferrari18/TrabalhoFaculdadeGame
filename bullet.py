import pygame
import math
import os


class Bala(pygame.sprite.Sprite):
    imagem_base = None

    def __init__(self, x, y, destino_x, destino_y):
        super().__init__()

        caminho = "assets/projectile/bullet.png"

        # --- CARREGAMENTO DO MOLDE ---
        if Bala.imagem_base is None:
            if os.path.exists(caminho):
                Bala.imagem_base = pygame.image.load(caminho).convert_alpha()
                Bala.imagem_base = pygame.transform.scale(Bala.imagem_base, (30, 15))
            else:
                # Se não achar a imagem, cria um rastro de luz ciano (Azul Água)
                Bala.imagem_base = pygame.Surface((20, 5))
                Bala.imagem_base.fill((0, 255, 255))

        # --- CÁLCULO DE ÂNGULO E ROTAÇÃO ---
        angulo_rad = math.atan2(destino_y - y, destino_x - x)
        angulo_graus = math.degrees(-angulo_rad)

        self.image = pygame.transform.rotate(Bala.imagem_base, angulo_graus)
        self.rect = self.image.get_rect(center=(x, y))
        self.dano = 30

        velocidade_tiro = 20
        self.vx = math.cos(angulo_rad) * velocidade_tiro
        self.vy = math.sin(angulo_rad) * velocidade_tiro

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy

        # Limites da tela 1365x768
        if (self.rect.left > 1365 + 100 or
                self.rect.right < -100 or
                self.rect.top > 768 + 100 or
                self.rect.bottom < -100):
            self.kill()