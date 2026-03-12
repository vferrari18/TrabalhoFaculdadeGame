import pygame  # Importa a biblioteca gráfica do Pygame


class Cenario:  # Classe responsável por gerenciar o fundo do jogo
    def __init__(self, L, A):  # Função de criação que recebe a Largura (L) e Altura (A) da tela
        self.scroll = 0  # Variável que acumula o quanto o cenário já andou para trás

        self.ceu = pygame.Surface((L, A)).convert()  # Cria uma imagem em branco do tamanho da tela inteira
        self.ceu.fill((135, 206, 235))  # Pinta essa imagem com um tom de Azul Céu

        # Cria a camada de montanhas para o efeito Parallax.
        # SRCALPHA permite que a imagem tenha transparência (fundo vazado)
        self.montanha = pygame.Surface((L, 300), pygame.SRCALPHA).convert_alpha()
        self.montanha.fill((100, 100, 100, 150))  # Pinta de Cinza com um pouco de transparência

    # --- ESTA É A LINHA QUE CORRIGE O ERRO ---
    # Agora ela aceita o 'self' (padrão), a 'tela', e o 'movimento' enviado pela Main.py
    def desenhar(self, tela, movimento):
        self.scroll += movimento  # Soma a velocidade do jogador ao scroll contínuo do cenário

        tela.blit(self.ceu, (0, 0))  # Desenha o céu fixo no fundo, começando da coordenada (0,0)

        # Cria o efeito Parallax (ilusão de profundidade)
        # O loop repete 3 vezes para desenhar a montanha lado a lado e cobrir buracos
        for i in range(3):
            # Matemática do Parallax: A montanha move a 30% (0.3) da velocidade real do jogo.
            # O símbolo % (módulo) faz a montanha se repetir infinitamente quando sai da tela.
            pos_x = (i * 800) - (self.scroll * 0.3) % 800
            tela.blit(self.montanha, (pos_x, 250))  # Desenha a montanha na tela na posição calculada


class Chao(pygame.sprite.Sprite):  # Classe do Chão físico onde o jogador pisa (herda de Sprite)
    def __init__(self, x, y, L):  # Recebe posição x, y e a Largura total do chão
        super().__init__()  # Inicia as mecânicas de Sprite (como a caixa de colisão)
        self.image = pygame.Surface((L, 100)).convert()  # Cria um bloco retangular para o chão
        self.image.fill((139, 69, 19))  # Pinta com a cor Marrom (terra)

        # Cria a caixa de colisão (rect) e posiciona a ponta superior esquerda (topleft) no x e y informados
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, tela, scroll_global):  # Função para desenhar o chão
        # O chão se move a 100% da velocidade (scroll_global) para acompanhar os pés do jogador
        pos_x = self.rect.x - scroll_global % self.rect.width

        # Desenha o primeiro bloco de chão
        tela.blit(self.image, (pos_x, self.rect.y))

        # Desenha um segundo bloco de chão colado logo atrás do primeiro para criar o chão infinito
        tela.blit(self.image, (pos_x + self.rect.width, self.rect.y))