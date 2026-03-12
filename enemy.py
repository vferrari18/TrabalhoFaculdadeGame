import pygame  # Importa o motor gráfico
import random  # Importa o gerador de números aleatórios


class Inimigo(pygame.sprite.Sprite):
    # --- NOVO: Variável de Classe (O Molde) ---
    # Fica fora do __init__, então pertence à "Ideia" de inimigo e não a um inimigo só
    molde_imagem = None

    def __init__(self, L, Y):
        super().__init__()

        # Se o molde ainda está vazio (nenhum inimigo nasceu ainda)...
        if Inimigo.molde_imagem is None:
            # Criamos a imagem pesada APENAS UMA VEZ
            Inimigo.molde_imagem = pygame.Surface((50, 50)).convert()
            Inimigo.molde_imagem.fill((255, 0, 0))

        # O inimigo atual simplesmente usa a imagem que já está pronta na memória!
        # Isso acaba com o travamento instantaneamente.
        self.image = Inimigo.molde_imagem

        self.rect = self.image.get_rect()
        self.vida = 60

        # Nasce fora da tela à direita com distância aleatória
        self.rect.x = L + random.randint(10, 150)
        self.rect.bottom = Y
        self.vel = random.randint(3, 5)

    def update(self):
        self.rect.x -= self.vel
        if self.rect.right < 0:
            self.kill()