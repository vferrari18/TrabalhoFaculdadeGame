import pygame


class Jogador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # --- CONFIGURAÇÃO DE CAMINHO ---
        caminho = "assets/player/"

        # --- CARREGAMENTO DAS IMAGENS ---
        self.img_parado = pygame.image.load(caminho + "parado.png").convert_alpha()
        self.img_parado = pygame.transform.scale(self.img_parado, (120, 140))
        self.frames_corrida = []
        for i in range(1, 7):
            img = pygame.image.load(f"{caminho}correndo{i}.png").convert_alpha()
            img = pygame.transform.scale(img, (120, 140))
            self.frames_corrida.append(img)

        # --- VARIÁVEIS DE CONTROLE DE ANIMAÇÃO ---
        self.index_anim = 0.0
        self.vel_anim = 0.15
        self.image = self.img_parado
        self.rect = self.image.get_rect()

        # --- STATUS E FÍSICA ---
        self.rect.x, self.rect.y = 100, 300
        self.vida = 100
        self.imune = 0
        self.vel_x = 0
        self.vel_y = 0
        self.gravidade = 0.8
        self.no_chao = False

    def animar(self):
        if self.vel_x != 0:
            self.index_anim += self.vel_anim

            if self.index_anim >= len(self.frames_corrida):
                self.index_anim = 0

            self.image = self.frames_corrida[int(self.index_anim)]

            if self.vel_x < 0:
                self.image = pygame.transform.flip(self.image, True, False)
        else:
            self.image = self.img_parado
            self.index_anim = 0

    def update(self, plataformas):
        self.vel_x = 0
        teclas = pygame.key.get_pressed()

        if teclas[pygame.K_a]: self.vel_x = -7
        if teclas[pygame.K_d]: self.vel_x = 7
        if (teclas[pygame.K_w] or teclas[pygame.K_SPACE]) and self.no_chao:
            self.vel_y = -15
            self.no_chao = False

        self.vel_y += self.gravidade
        self.rect.y += self.vel_y

        for p in plataformas:
            if self.rect.colliderect(p.rect):
                # Se o pé do jogador passar da 'linha_dos_pes' (68px dentro do chão)
                if self.rect.bottom >= p.linha_dos_pes and self.vel_y > 0:
                    self.rect.bottom = p.linha_dos_pes
                    self.vel_y = 0
                    self.no_chao = True

        if self.imune > 0: self.imune -= 1

        self.animar()

    def draw(self, tela):
        if self.imune > 0 and self.imune % 4 < 2:
            return
        tela.blit(self.image, self.rect)