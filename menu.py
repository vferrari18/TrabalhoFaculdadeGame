import pygame  # Importa o motor gráfico
import sys  # Importa funções de encerramento do sistema
from score_manager import ler_scores  # Importa a função que lê o ranking do arquivo


def menu_principal():  # Função do menu que você já tinha
    pygame.init()  # Inicializa o Pygame
    tela = pygame.display.set_mode((800, 600))  # Define o tamanho da janela
    fonte_menu = pygame.font.SysFont("Arial", 40, bold=True)  # Fonte das opções
    fonte_inst = pygame.font.SysFont("Arial", 20)  # Fonte das instruções

    # Define as áreas dos botões para o clique do mouse
    btn_start = pygame.Rect(300, 220, 200, 50)
    btn_pontos = pygame.Rect(300, 300, 200, 50)
    btn_sair = pygame.Rect(300, 380, 200, 50)

    while True:  # Loop do Menu
        tela.fill((30, 30, 30))  # Fundo cinza escuro
        mouse = pygame.mouse.get_pos()  # Localização do mouse

        # Desenha os botões e muda a cor se o mouse estiver sobre eles
        cor_s = (255, 255, 0) if btn_start.collidepoint(mouse) else (255, 255, 255)
        cor_p = (255, 255, 0) if btn_pontos.collidepoint(mouse) else (255, 255, 255)
        cor_x = (255, 255, 0) if btn_sair.collidepoint(mouse) else (255, 255, 255)

        tela.blit(fonte_menu.render("START", True, cor_s), (340, 220))
        tela.blit(fonte_menu.render("RANKING", True, cor_p), (320, 300))
        tela.blit(fonte_menu.render("SAIR", True, cor_x), (355, 380))

        # REQUISITO: Instruções de controle visíveis no menu
        inst = fonte_inst.render("WASD: Mover | MOUSE: Atirar", True, (200, 200, 200))
        tela.blit(inst, (280, 520))

        for e in pygame.event.get():  # Captura eventos
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:  # Se clicou
                if btn_start.collidepoint(mouse): return "jogar"
                if btn_pontos.collidepoint(mouse): return "pontos"
                if btn_sair.collidepoint(mouse): pygame.quit(); sys.exit()

        pygame.display.update()  # Atualiza o quadro


def exibir_ranking(tela):  # Nova função para mostrar os melhores jogadores
    fonte = pygame.font.SysFont("Arial", 30)  # Fonte para a lista
    while True:  # Loop da tela de ranking
        tela.fill((10, 10, 10))  # Fundo quase preto
        scores = ler_scores()  # Busca a lista ordenada

        titulo = fonte.render("TOP 5 MELHORES JOGADORES", True, (255, 255, 0))
        tela.blit(titulo, (200, 50))

        # Mostra apenas os 5 melhores
        for i, item in enumerate(scores[:5]):
            txt = f"{i + 1}º - {item['nome']}: {item['kills']} Kills"
            tela.blit(fonte.render(txt, True, (255, 255, 255)), (250, 150 + (i * 50)))

        tela.blit(fonte.render("Pressione ESC para voltar", True, (150, 150, 150)), (250, 500))

        for e in pygame.event.get():  # Captura saída da tela
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE: return  # Volta ao menu principal
        pygame.display.update()