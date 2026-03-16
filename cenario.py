import pygame


class Cenario:
    def __init__(self, L, A):
        self.L = L
        self.A = A
        caminho = "assets/scenario/"
        self.img_ceu = pygame.image.load(caminho + "ceu.png").convert()
        self.img_ceu = pygame.transform.scale(self.img_ceu, (L, A))
        self.img_montanha = pygame.image.load(caminho + "montanhas.png").convert_alpha()
        self.img_montanha = pygame.transform.scale(self.img_montanha, (L, A))
        self.scroll_ceu = 0
        self.scroll_montanha = 0
        self.scroll_chao = 0

    def desenhar(self, tela, mov_player):
        self.scroll_ceu += 0.5
        self.scroll_montanha += mov_player * 0.2
        self.scroll_chao += mov_player

        # Desenho do Céu e Montanhas (Módulo % L)
        pos_ceu = self.scroll_ceu % self.L
        tela.blit(self.img_ceu, (-pos_ceu, 0))
        tela.blit(self.img_ceu, (self.L - pos_ceu, 0))

        pos_mon = self.scroll_montanha % self.L
        tela.blit(self.img_montanha, (-pos_mon, 0))
        tela.blit(self.img_montanha, (self.L - pos_mon, 0))


class Chao(pygame.sprite.Sprite):
    def __init__(self, x, y, L):
        super().__init__()
        caminho = "assets/scenario/"
        self.image_original = pygame.image.load(caminho + "chao.png").convert_alpha()
        self.image = pygame.transform.scale(self.image_original, (L, 224))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.linha_dos_pes = self.rect.top + 68

    def draw(self, tela, scroll_global):
        pos_x = -(scroll_global % self.rect.width)
        tela.blit(self.image, (pos_x, self.rect.y))
        tela.blit(self.image, (pos_x + self.rect.width, self.rect.y))