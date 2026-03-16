import pygame
import random
import os


class Inimigo(pygame.sprite.Sprite):
    def __init__(self, L, topo_chao):
        super().__init__()
        caminho = "assets/enemy/"
        self.frames = []

        # --- CARREGAMENTO FLEXÍVEL ---
        for i in range(1, 7):
            img_nome = f"aranha{i}.png"
            caminho_completo = os.path.join(caminho, img_nome)

            if os.path.exists(caminho_completo):
                img = pygame.image.load(caminho_completo).convert_alpha()
                img = pygame.transform.scale(img, (200, 120))
                self.frames.append(img)

        # Se não achar NENHUMA imagem, cria um bloco reserva para o jogo não fechar
        if not self.frames:
            placeholder = pygame.Surface((100, 60))
            placeholder.fill((255, 50, 50))
            self.frames.append(placeholder)

        self.index_anim = 0.0
        self.image = self.frames[0]
        self.rect = self.image.get_rect()

        # --- POSICIONAMENTO NA ESTRADA ---
        self.rect.x = L + random.randint(100, 600)
        self.rect.bottom = topo_chao + 68

        self.vida = 60
        self.vel = random.randint(4, 7)

    def update(self):
        # Movimento para a esquerda
        self.rect.x -= self.vel

        # Animação automática (só ocorre se houver mais de 1 frame)
        if len(self.frames) > 1:
            self.index_anim += 0.15
            if self.index_anim >= len(self.frames):
                self.index_anim = 0
            self.image = self.frames[int(self.index_anim)]

        # Se sair da tela, desaparece
        if self.rect.right < 0:
            self.kill()