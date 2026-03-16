import pygame  # Importa a biblioteca do jogo
import sys  # Importa funções para fechar o programa
from score_manager import ler_scores  # Importa a função que busca os pontos salvos


def exibir_ranking(tela):
    fonte = pygame.font.SysFont("Arial", 40, bold=True)
    fonte_lista = pygame.font.SysFont("Arial", 30)

    while True:
        tela.fill((10, 10, 10))
        scores = ler_scores()

        titulo = fonte.render("TOP 5 MELHORES JOGADORES", True, (255, 255, 0))
        tela.blit(titulo, (1365 // 2 - titulo.get_width() // 2, 50))

        for i, item in enumerate(scores[:5]):
            texto = f"{i + 1}º - {item['nome']}: {item['kills']} Kills"
            img_texto = fonte_lista.render(texto, True, (255, 255, 255))
            tela.blit(img_texto, (1365 // 2 - 150, 150 + (i * 60)))

        voltar = fonte_lista.render("Pressione ESC para voltar ao Menu", True, (150, 150, 150))
        tela.blit(voltar, (1365 // 2 - voltar.get_width() // 2, 600))

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit();
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    return

        pygame.display.update()


def menu_principal():
    LARGURA, ALTURA = 1365, 768
    tela = pygame.display.set_mode((LARGURA, ALTURA))

    # --- NOVO: LÓGICA DE MÚSICA DO MENU ---
    pygame.mixer.music.load("assets/sounds/menu_bgm.mp3")
    pygame.mixer.music.set_volume(0.5)  # Volume em 50%
    pygame.mixer.music.play(-1)  # O parâmetro -1 faz a música tocar em loop infinito
    # --------------------------------------

    try:
        caminho_menu = "assets/menu/menu_bg.png"
        fundo = pygame.image.load(caminho_menu).convert()
        fundo = pygame.transform.scale(fundo, (LARGURA, ALTURA))
    except:
        fundo = pygame.Surface((LARGURA, ALTURA))
        fundo.fill((0, 0, 50))

    fonte_botao = pygame.font.SysFont("Arial", 35, bold=True)

    # --- NOVO: Fonte para as instruções de teclas ---
    fonte_instrucoes = pygame.font.SysFont("Arial", 11, bold=True)

    btn_start_rect = pygame.Rect(530, 346, 300, 80)
    btn_rank_rect = pygame.Rect(530, 475, 300, 60)
    btn_sair_rect = pygame.Rect(530, 565, 300, 60)

    while True:
        tela.blit(fundo, (0, 0))
        mouse = pygame.mouse.get_pos()

        cor_s = (0, 255, 255) if btn_start_rect.collidepoint(mouse) else (255, 255, 255)
        cor_r = (0, 255, 255) if btn_rank_rect.collidepoint(mouse) else (255, 255, 255)
        cor_x = (255, 255, 0) if btn_sair_rect.collidepoint(mouse) else (255, 255, 255)

        txt_start = fonte_botao.render("JOGAR", True, cor_s)
        txt_rank = fonte_botao.render("RANKING", True, cor_r)
        txt_sair = fonte_botao.render("SAIR", True, cor_x)

        tela.blit(txt_start, (btn_start_rect.centerx - txt_start.get_width() // 2,
                              btn_start_rect.centery - txt_start.get_height() // 2))
        tela.blit(txt_rank, (btn_rank_rect.centerx - txt_rank.get_width() // 2,
                             btn_rank_rect.centery - txt_rank.get_height() // 2))
        tela.blit(txt_sair, (btn_sair_rect.centerx - txt_sair.get_width() // 2,
                             btn_sair_rect.centery - txt_sair.get_height() // 2))

        # --- NOVO: Desenho das Teclas no Rodapé ---
        teclas_texto = "CONTROLES - WASD: MOVER | ESPAÇO: PULAR | MOUSE: ATIRAR"
        img_teclas = fonte_instrucoes.render(teclas_texto, True, (200, 200, 200))
        # Posiciona centralizado horizontalmente e a 720 pixels de altura
        tela.blit(img_teclas, (LARGURA // 2 - img_teclas.get_width() // 2, 735))

        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                if btn_start_rect.collidepoint(mouse): return "jogar"
                if btn_rank_rect.collidepoint(mouse): return "pontos"
                if btn_sair_rect.collidepoint(mouse): pygame.quit(); sys.exit()

        pygame.display.update()