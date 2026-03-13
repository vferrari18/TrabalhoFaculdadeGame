import pygame
import sys
import random
# Importando as funções dos seus outros arquivos
from menu import menu_principal, exibir_ranking
from player import Jogador
from cenario import Cenario, Chao
from bullet import Bala
from enemy import Inimigo
from score_manager import salvar_score

# --- CONFIGURAÇÕES GLOBAIS ---
LARGURA, ALTURA = 1365, 768


def tela_input_nome(tela):  # Passamos a tela como argumento para ser mais seguro
    nome = ""
    fonte = pygame.font.SysFont("Arial", 40, bold=True)
    rodando_input = True

    while rodando_input:
        tela.fill((0, 0, 0))
        # Instruções na tela
        img_pergunta = fonte.render("DIGITE SEU NOME E APERTE ENTER:", True, (255, 255, 255))
        img_nome = fonte.render(nome + "|", True, (255, 255, 0))

        tela.blit(img_pergunta, (LARGURA // 2 - img_pergunta.get_width() // 2, 250))
        tela.blit(img_nome, (LARGURA // 2 - img_nome.get_width() // 2, 350))

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit();
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN:
                    if len(nome) > 0: return nome  # Só sai se tiver digitado algo
                elif e.key == pygame.K_BACKSPACE:
                    nome = nome[:-1]
                else:
                    if len(nome) < 12:  # Limite de caracteres
                        nome += e.unicode

        pygame.display.update()


def rodar_jogo(nome_player, tela):  # Recebe a tela para não criar várias janelas
    relogio = pygame.time.Clock()
    p = Jogador()
    f = Cenario(LARGURA, ALTURA)
    chao = Chao(0, 544, LARGURA)  # 768 - 224 = 544
    balas = pygame.sprite.Group()
    inimigos = pygame.sprite.Group()

    spawn_timer = 0
    score = 0
    tempo_fase = 40000  # 40 segundos
    estado = "JOGANDO"
    fonte_hud = pygame.font.SysFont("Arial", 24, bold=True)

    while True:  # Loop da fase
        dt = relogio.tick(60)
        mov = 0

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit();
                sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN and estado == "JOGANDO":
                mx, my = pygame.mouse.get_pos()
                balas.add(Bala(p.rect.centerx, p.rect.centery, mx, my))
            if e.type == pygame.MOUSEBUTTONDOWN and estado != "JOGANDO":
                salvar_score(nome_player, score)
                return  # Volta para o Main (que chamará o menu)

        if estado == "JOGANDO":
            tempo_fase -= dt
            if tempo_fase <= 0:
                tempo_fase = 0
                estado = "VITORIA"

            p.update([chao])

            # --- NOVA CÂMERA DINÂMICA ---
            meio_tela = LARGURA // 2

            if p.vel_x > 0:  # Se o jogador estiver indo para a direita
                mov = p.vel_x  # O CENÁRIO SEMPRE SE MOVE

                # O jogador só avança na tela se ainda não chegou no meio
                if p.rect.centerx < meio_tela:
                    p.rect.x += p.vel_x
                else:
                    p.rect.centerx = meio_tela  # Trava no meio, mas o 'mov' continua empurrando o fundo

            elif p.vel_x < 0:  # Se o jogador estiver indo para a esquerda
                p.rect.x += p.vel_x  # Ele anda normalmente para trás
                if p.rect.left < 0:
                    p.rect.left = 0  # Mas o cenário NÃO se move para a esquerda (padrão Metal Slug)
            # -----------------------------

            # Spawn Inimigos
            spawn_timer += dt
            if spawn_timer > 1500:
                for _ in range(random.randint(1, 2)):
                    inimigos.add(Inimigo(LARGURA, chao.rect.top))
                spawn_timer = 0

            balas.update()
            inimigos.update()

            # Colisões
            colis = pygame.sprite.groupcollide(balas, inimigos, True, False)
            for b, atingidos in colis.items():
                for i in atingidos:
                    i.vida -= b.dano
                    if i.vida <= 0: i.kill(); score += 1

            if p.imune <= 0 and pygame.sprite.spritecollide(p, inimigos, False):
                p.vida -= 20
                p.imune = 60
                if p.vida <= 0: estado = "GAME_OVER"

        # DESENHO
        f.desenhar(tela, mov)
        chao.draw(tela, f.scroll_chao) # Agora usamos o scroll específico do chão
        for b in balas: tela.blit(b.image, b.rect)
        inimigos.draw(tela)
        p.draw(tela)

        # HUD
        tempo_seg = int(tempo_fase / 1000)
        info = f"PLAYER: {nome_player} | VIDA: {p.vida} | KILLS: {score} | TEMPO: {tempo_seg}s"
        tela.blit(fonte_hud.render(info, True, (255, 255, 255)), (20, 20))

        if estado != "JOGANDO":
            msg = "MISSÃO CUMPRIDA!" if estado == "VITORIA" else "FIM DO JOGO"
            cor = (0, 255, 0) if estado == "VITORIA" else (255, 0, 0)
            img_fim = pygame.font.SysFont("Arial", 80, bold=True).render(msg, True, cor)
            tela.blit(img_fim, (LARGURA // 2 - img_fim.get_width() // 2, ALTURA // 2 - 50))

        pygame.display.update()


def main():
    pygame.init()
    # Criamos a tela uma única vez aqui na Main
    tela_global = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Firefall 2D - UNINTER 2025")

    while True:  # O Loop que impede o "Exit Code 0"
        escolha = menu_principal()  # O menu roda usando a tela global internamente

        if escolha == "jogar":
            nome = tela_input_nome(tela_global)
            rodar_jogo(nome, tela_global)
        elif escolha == "pontos":
            exibir_ranking(tela_global)
        else:
            # Caso o menu retorne algo inesperado, evita fechar o programa
            pass


if __name__ == "__main__":
    main()  # Inicia o programa