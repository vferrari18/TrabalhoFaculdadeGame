import pygame, sys, random  # Importa as bibliotecas para o motor, sistema e sorteios
from menu import menu_principal, exibir_ranking  # Importa as telas do menu
from player import Jogador  # Importa a classe do herói
from cenario import Cenario, Chao  # Importa o mundo e as plataformas
from bullet import Bala  # Importa a lógica de tiro
from enemy import Inimigo  # Importa os adversários
from score_manager import salvar_score  # Importa a função para persistência de dados

# Inicialização e Configurações de Janela
pygame.init()  # Liga o motor do Pygame
tela = pygame.display.set_mode((800, 600))  # Cria a janela de 800x600 pixels
pygame.display.set_caption("Metal Slug Clone - Uninter 2025")  # Título da janela
relogio = pygame.time.Clock()  # Controlador de FPS (quadros por segundo)

# Fontes para a Interface do Usuário (HUD)
fonte_hud = pygame.font.SysFont("Arial", 24, bold=True)  # Fonte para vida, tempo e score
fonte_grande = pygame.font.SysFont("Arial", 60, bold=True)  # Fonte para mensagens de fim


def tela_input_nome():  # Função para capturar o nome do jogador antes da partida
    nome = ""  # Nome começa vazio
    fonte = pygame.font.SysFont("Arial", 40)  # Fonte para o campo de digitação
    while True:  # Loop da tela de texto
        tela.fill((0, 0, 0))  # Fundo preto
        tela.blit(fonte.render("DIGITE SEU NOME E ENTER:", True, (255, 255, 255)), (150, 200))
        tela.blit(fonte.render(nome + "|", True, (255, 255, 0)), (320, 300))  # Cursor visual
        for e in pygame.event.get():  # Captura as teclas
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN and len(nome) > 0:
                    return nome  # Confirma
                elif e.key == pygame.K_BACKSPACE:
                    nome = nome[:-1]  # Apaga
                elif len(nome) < 10:
                    nome += e.unicode  # Adiciona letra (máx 10)
        pygame.display.update()


def rodar_jogo(nome_player):  # Função principal da jogabilidade
    p = Jogador()  # Cria o jogador
    f = Cenario(800, 600)  # Cria o cenário parallax
    chao = Chao(0, 550, 800)  # Cria o chão
    balas, inimigos = pygame.sprite.Group(), pygame.sprite.Group()  # Grupos de sprites

    spawn_timer, score = 0, 0  # Cronômetro de inimigos e placar de mortes

    # --- NOVO: Lógica de Tempo da Fase ---
    tempo_fase = 40000  # 40 segundos convertidos para milissegundos
    # -------------------------------------

    estado = "JOGANDO"  # Pode ser "JOGANDO", "GAME_OVER" ou "VITORIA"

    while True:  # Loop principal do frame
        tela.fill((0, 0, 0))  # Limpa a tela
        dt = relogio.tick(60)  # Trava 60 FPS e retorna o tempo desde o último frame
        mov = 0  # Movimento do cenário inicia em zero

        # --- GESTÃO DE CLIQUES E SAÍDA ---
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN and estado == "JOGANDO":
                mx, my = pygame.mouse.get_pos()
                balas.add(Bala(p.rect.centerx, p.rect.centery, mx, my))  # Atira
            if e.type == pygame.MOUSEBUTTONDOWN and estado != "JOGANDO":
                salvar_score(nome_player, score)  # Salva o rank ao sair
                return  # Volta ao menu

        # --- LÓGICA DE JOGO ATIVO ---
        if estado == "JOGANDO":
            # Atualiza o cronômetro da fase
            tempo_fase -= dt  # Diminui os milissegundos passados
            if tempo_fase <= 0:
                tempo_fase = 0
                estado = "VITORIA"  # Se o tempo acabar, o jogador vence!

            p.update([chao])  # Atualiza física e colisão do player
            if p.rect.centerx >= 400 and p.vel_x > 0:
                p.rect.centerx = 400;
                mov = p.vel_x  # Câmera fixa no meio
            else:
                p.rect.x += p.vel_x  # Caminhada livre
                if p.rect.left < 0: p.rect.left = 0  # Limite esquerdo da tela

            # Spawn de inimigos a cada 1.5s
            spawn_timer += dt
            if spawn_timer > 1500:
                for _ in range(random.randint(1, 2)):
                    inimigos.add(Inimigo(800, chao.rect.top))
                spawn_timer = 0

            balas.update();
            inimigos.update()  # Move objetos

            # Colisão Bala vs Inimigo
            colis = pygame.sprite.groupcollide(balas, inimigos, True, False)
            for b, atingidos in colis.items():
                for i in atingidos:
                    i.vida -= b.dano
                    if i.vida <= 0: i.kill(); score += 1

            # Colisão Player vs Inimigo (Dano e Imunidade)
            if p.imune <= 0 and pygame.sprite.spritecollide(p, inimigos, False):
                p.vida -= 20;
                p.imune = 60
                if p.vida <= 0: estado = "GAME_OVER"

        # --- DESENHO NA TELA ---
        f.desenhar(tela, mov);
        chao.draw(tela, f.scroll)  # Fundo e Chão
        for b in balas: tela.blit(b.image, b.rect)  # Tiros
        inimigos.draw(tela);
        p.draw(tela)  # Inimigos e Jogador

        # HUD: Informações em tempo real
        tempo_segundos = int(tempo_fase / 1000)  # Converte ms para segundos inteiros
        info = f"{nome_player} | VIDA: {p.vida} | KILLS: {score} | TEMPO: {tempo_segundos}s"
        tela.blit(fonte_hud.render(info, True, (255, 255, 255)), (10, 10))

        # Telas de Fim de Jogo
        if estado == "GAME_OVER":
            txt = fonte_grande.render("FIM DO JOGO", True, (255, 0, 0))
            tela.blit(txt, (400 - txt.get_width() // 2, 250))
        elif estado == "VITORIA":
            txt = fonte_grande.render("MISSÃO CUMPRIDA!", True, (0, 255, 0))
            tela.blit(txt, (400 - txt.get_width() // 2, 250))

        pygame.display.update()  # Mostra o frame atualizado


def main():  # Gerenciador de estados do menu
    while True:
        escolha = menu_principal()
        if escolha == "jogar":
            nome = tela_input_nome()
            rodar_jogo(nome)
        elif escolha == "pontos":
            exibir_ranking(tela)


if __name__ == "__main__":
    main()