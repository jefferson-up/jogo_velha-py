import pygame
import sys

pygame.init()

# Constantes
LARGURA, ALTURA = 600, 600
ESPACO = 200
FUND0_COR = (230, 232, 250)
LINHA_COR = (0, 0, 0)
STATUS_FONTE = pygame.font.Font(None, 30)
VITORIA_FONTE = pygame.font.Font(None, 60)

# Carregando imagens e sons
fundo_tabuleiro = pygame.image.load('files/fundo_tabuleiro.png')
fundo_tabuleiro = pygame.transform.scale(fundo_tabuleiro, (LARGURA, ALTURA))
mickey_image = pygame.image.load('files/minnie.png')
minnie_image = pygame.image.load('files/mickey.png')
mickey_image = pygame.transform.scale(mickey_image, (ESPACO, ESPACO))
minnie_image = pygame.transform.scale(minnie_image, (ESPACO, ESPACO))
clique_som = pygame.mixer.Sound('files/clique.wav')
vitoria_som = pygame.mixer.Sound('files/vitoria.mp3')

# Inicialização da Tela
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption('Jogo da Velha - Disney')
tela.fill(FUND0_COR)

# Estado inicial do jogo
tabuleiro = [["" for _ in range(3)] for _ in range(3)]
vez_do_jogador = True
jogo_rodando = True
vencedor = None
pontuacao_mickey = 0
pontuacao_minnie = 0

# Funções do Jogo
def desenhar_tabuleiro():
    tela.fill(FUND0_COR)
    tela.blit(fundo_tabuleiro, (0, 0))
    for i in range(1, 3):
        pygame.draw.line(tela, LINHA_COR, (i * ESPACO, 0), (i * ESPACO, ALTURA), 3)
        pygame.draw.line(tela, LINHA_COR, (0, i * ESPACO), (LARGURA, i * ESPACO), 3)

def marcar_quadro(row, col, jogador):
    tabuleiro[row][col] = jogador

def desenhar_marcacoes():
    for row in range(3):
        for col in range(3):
            if tabuleiro[row][col] == 'X':
                tela.blit(mickey_image, (col * ESPACO, row * ESPACO))
            elif tabuleiro[row][col] == 'O':
                tela.blit(minnie_image, (col * ESPACO, row * ESPACO))

def verificar_vitoria(jogador):
    # Verifica linhas, colunas e diagonais
    for row in range(3):
        if tabuleiro[row][0] == tabuleiro[row][1] == tabuleiro[row][2] == jogador:
            return True
    for col in range(3):
        if tabuleiro[0][col] == tabuleiro[1][col] == tabuleiro[2][col] == jogador:
            return True
    if tabuleiro[0][0] == tabuleiro[1][1] == tabuleiro[2][2] == jogador or \
       tabuleiro[0][2] == tabuleiro[1][1] == tabuleiro[2][0] == jogador:
        return True
    return False

def verificar_empate():
    for row in range(3):
        for col in range(3):
            if tabuleiro[row][col] == "":
                return False
    return True

def minimax(tabuleiro, jogador):
    if verificar_vitoria('O'):
        return {'pontuacao': 1}
    if verificar_vitoria('X'):
        return {'pontuacao': -1}
    if verificar_empate():
        return {'pontuacao': 0}

    if jogador == 'O':
        melhor = {'pontuacao': -float('inf')}
    else:
        melhor = {'pontuacao': float('inf')}

    for row in range(3):
        for col in range(3):
            if tabuleiro[row][col] == "":
                tabuleiro[row][col] = jogador
                pontuacao = minimax(tabuleiro, 'X' if jogador == 'O' else 'O')
                tabuleiro[row][col] = ""
                pontuacao['row'], pontuacao['col'] = row, col

                if jogador == 'O':
                    if pontuacao['pontuacao'] > melhor['pontuacao']:
                        melhor = pontuacao
                else:
                    if pontuacao['pontuacao'] < melhor['pontuacao']:
                        melhor = pontuacao

    return melhor

def jogada_ia():
    if verificar_empate() or verificar_vitoria('X') or verificar_vitoria('O'):
        return

    jogada = minimax(tabuleiro, 'O')
    marcar_quadro(jogada['row'], jogada['col'], 'O')

def celulas_vazias():
    return [(row, col) for row in range(3) for col in range(3) if tabuleiro[row][col] == ""]

def reiniciar():
    global tabuleiro, vez_do_jogador, jogo_rodando, vencedor
    tabuleiro = [["" for _ in range(3)] for _ in range(3)]
    vez_do_jogador = True
    jogo_rodando = True
    vencedor = None
    desenhar_tabuleiro()
    desenhar_marcacoes()

# Função para obter o nome do jogador
def obter_nome_jogador():
    tela.fill(FUND0_COR)
    fonte = pygame.font.Font(None, 36)
    input_box = pygame.Rect(50, 150, 200, 50)
    cor_fundo = pygame.Color('white')
    cor_texto = pygame.Color('black')
    prompt_texto = fonte.render('Digite seu nome e pressione Enter', True, cor_texto)
    nome = ""
    ativo = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    ativo = not ativo
                else:
                    ativo = False
                cor_fundo = pygame.Color('gray' if ativo else 'white')
            if event.type == pygame.KEYDOWN:
                if ativo:
                    if event.key == pygame.K_RETURN:
                        return nome
                    elif event.key == pygame.K_BACKSPACE:
                        nome = nome[:-1]
                    else:
                        nome += event.unicode

        tela.fill(FUND0_COR)
        tela.blit(prompt_texto, (50, 100))
        input_text = fonte.render(nome, True, cor_texto)
        largura = max(200, input_text.get_width() + 10)
        input_box.w = largura
        tela.blit(input_text, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(tela, cor_fundo, input_box, 2)

        pygame.display.flip()

# Obter nomes dos jogadores
nome_jogador = obter_nome_jogador()
nome_ia = "Mickey Mouse"

# Função para desenhar botões
def desenhar_botao(texto, rect, cor_fundo, cor_texto):
    pygame.draw.rect(tela, cor_fundo, rect)
    texto_surface = STATUS_FONTE.render(texto, True, cor_texto)
    tela.blit(texto_surface, (rect.x + (rect.width - texto_surface.get_width()) / 2, rect.y + (rect.height - texto_surface.get_height()) / 2))

def botao_clicado(rect):
    posicao_mouse = pygame.mouse.get_pos()
    return rect.collidepoint(posicao_mouse)

# Função para adicionar botões gráficos
def adicionar_botoes():
    reiniciar_botao = pygame.Rect(50, ALTURA - 70, 100, 50)
    sair_botao = pygame.Rect(LARGURA - 150, ALTURA - 70, 100, 50)
    
    desenhar_botao('Reiniciar', reiniciar_botao, (0, 255, 0), (255, 255, 255))
    desenhar_botao('Sair', sair_botao, (255, 0, 0), (255, 255, 255))

    posicao_mouse = pygame.mouse.get_pos()
    if pygame.mouse.get_pressed()[0]:  # Verifica se o botão esquerdo do mouse foi pressionado
        if reiniciar_botao.collidepoint(posicao_mouse):
            reiniciar()
        elif sair_botao.collidepoint(posicao_mouse):
            pygame.quit()
            sys.exit()

# função para mostrar o placar
def mostrar_placar():
    placar_texto = STATUS_FONTE.render(f'Placar - {nome_jogador}: {pontuacao_mickey} | {nome_ia}: {pontuacao_minnie}', True, (0, 0, 0))
    tela.blit(placar_texto, (10, 10))

# loop principal que exibe de quem é a vez
while True:
    desenhar_tabuleiro()
    mostrar_placar()
    adicionar_botoes()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and vez_do_jogador and jogo_rodando:
            mouseX = event.pos[0]
            mouseY = event.pos[1]
            clicked_row = int(mouseY // ESPACO)
            clicked_col = int(mouseX // ESPACO)

            if tabuleiro[clicked_row][clicked_col] == "":
                marcar_quadro(clicked_row, clicked_col, 'X')
                clique_som.play()  # Reproduz som de clique
                if verificar_vitoria('X'):
                    vitoria_som.play()  # Reproduz som de vitória
                    vencedor = nome_jogador  
                    pontuacao_mickey += 1
                    jogo_rodando = False
                elif verificar_empate():
                    vencedor = 'Ninguém'
                    jogo_rodando = False
                else:
                    vez_do_jogador = False

    desenhar_marcacoes()
    pygame.display.update()
    
    # Exibir status do jogo
    if jogo_rodando:
        status_texto = STATUS_FONTE.render(f'Vez de: {nome_jogador if vez_do_jogador else nome_ia}', True, (0, 0, 0))
        tela.blit(status_texto, (10, ALTURA - 30))

    pygame.display.update()
    if not vez_do_jogador and jogo_rodando:
        jogada_ia()
        clique_som.play()  # Reproduz som de clique
        if verificar_vitoria('O'):
            vitoria_som.play()  # Reproduz som de vitória
            vencedor = nome_ia  # 
            pontuacao_minnie += 1
            jogo_rodando = False
        elif verificar_empate():
            vencedor = 'Ninguém'
            jogo_rodando = False
        else:
            vez_do_jogador = True

    

    if not jogo_rodando:
        texto_vitoria = VITORIA_FONTE.render(f'{vencedor} venceu!', True, (0, 255, 0))
        tela.blit(texto_vitoria, (LARGURA // 2 - texto_vitoria.get_width() // 2, ALTURA // 2 - texto_vitoria.get_height() // 2))
        pygame.display.update()
        pygame.time.wait(4000)  # Espera 4 segundos antes de reiniciar
        reiniciar()
