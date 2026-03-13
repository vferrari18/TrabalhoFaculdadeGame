import pygame  # Importa a biblioteca do motor de jogo


class Jogador(pygame.sprite.Sprite):  # Define a classe herdando as funções de Sprite
    def __init__(self):  # Função executada ao criar o objeto Jogador
        super().__init__()  # Ativa os recursos internos de Sprite do Pygame

        # --- CONFIGURAÇÃO DE CAMINHO ---
        caminho = "assets/player/"  # Define a pasta onde estão as imagens

        # --- CARREGAMENTO DAS IMAGENS ---
        # Carrega a imagem dele parado e converte (convert_alpha mantém transparência)
        # Redimensionamos de 180x210 para 60x70 para caber melhor na tela de 800x600
        self.img_parado = pygame.image.load(caminho + "parado.png").convert_alpha()
        self.img_parado = pygame.transform.scale(self.img_parado, (120, 140))

        # Criamos uma lista para carregar os 6 quadros da corrida
        self.frames_corrida = []
        for i in range(1, 7):  # Loop que vai de 1 até 6
            # Monta o nome: "assets/player/correndo1.png", "assets/player/correndo2.png", etc.
            img = pygame.image.load(f"{caminho}correndo{i}.png").convert_alpha()
            # Redimensiona cada quadro para manter o padrão
            img = pygame.transform.scale(img, (120, 140))
            self.frames_corrida.append(img)  # Adiciona à lista de animação

        # --- VARIÁVEIS DE CONTROLE DE ANIMAÇÃO ---
        self.index_anim = 0.0  # Contador para saber qual frame mostrar
        self.vel_anim = 0.15  # Velocidade da troca de quadros (ajuste para ficar natural)
        self.image = self.img_parado  # Imagem inicial
        self.rect = self.image.get_rect()  # Cria a caixa de colisão baseada na imagem de 60x70

        # --- STATUS E FÍSICA ---
        self.rect.x, self.rect.y = 100, 300  # Posição inicial no ar
        self.vida = 100
        self.imune = 0
        self.vel_x = 0
        self.vel_y = 0
        self.gravidade = 0.8
        self.no_chao = False

    def animar(self):  # Função que decide o desenho do personagem
        # Se o jogador estiver se movendo para os lados
        if self.vel_x != 0:
            self.index_anim += self.vel_anim  # Avança o contador

            # Se o contador passar do limite da lista (6), volta pro início
            if self.index_anim >= len(self.frames_corrida):
                self.index_anim = 0

            # Pega a imagem da lista (int remove os decimais: 0.15 vira 0, 1.2 vira 1...)
            self.image = self.frames_corrida[int(self.index_anim)]

            # Lógica de Espelhamento (Flip):
            if self.vel_x < 0:  # Se estiver indo para a esquerda (negativo)
                # Inverte a imagem horizontalmente para o boneco olhar para trás
                self.image = pygame.transform.flip(self.image, True, False)
        else:
            # Se não estiver se movendo horizontalmente, volta para a imagem de parado
            self.image = self.img_parado
            self.index_anim = 0  # Reseta a corrida para começar do primeiro passo depois

    def update(self, plataformas):  # Atualização constante (60x por segundo)
        self.vel_x = 0  # Zera a velocidade X para o controle ser preciso
        teclas = pygame.key.get_pressed()

        if teclas[pygame.K_a]: self.vel_x = -7  # Move Esquerda
        if teclas[pygame.K_d]: self.vel_x = 7  # Move Direita

        # Pulo
        if (teclas[pygame.K_w] or teclas[pygame.K_SPACE]) and self.no_chao:
            self.vel_y = -15
            self.no_chao = False

        # Aplica Gravidade e Movimento Y
        self.vel_y += self.gravidade
        self.rect.y += self.vel_y

        # Dentro do update do player, na parte de colisão:
        for p in plataformas:
            if self.rect.colliderect(p.rect):
                # Se o pé do jogador passar da 'linha_dos_pes' (68px dentro do chão)
                if self.rect.bottom >= p.linha_dos_pes and self.vel_y > 0:
                    self.rect.bottom = p.linha_dos_pes
                    self.vel_y = 0
                    self.no_chao = True

        # Reduz tempo de imunidade
        if self.imune > 0: self.imune -= 1

        # CHAMA A ANIMAÇÃO
        self.animar()

    def draw(self, tela):  # Desenha na tela principal
        # Efeito de piscar quando está imune (toma dano)
        if self.imune > 0 and self.imune % 4 < 2:
            return
        tela.blit(self.image, self.rect)