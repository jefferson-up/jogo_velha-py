import pygame
import sys

pygame.init()

# Constantes
LARGURA, ALTURA = 600, 600  # Dobrando o tamanho da tela
ESPACO = 200  # Ajustando o tamanho do espaço entre as linhas
FUND0_COR = (230, 232, 250)  # Cor de fundo
LINHA_COR = (0, 0, 0)  # Cor das linhas do tabuleiro
STATUS_FONTE = pygame.font.Font(None, 30)  # Fonte para o status do jogo
VITORIA_FONTE = pygame.font.Font(None, 60)  # Fonte para a mensagem de vitória

# Carregue aqui a imagem de fundo do tabuleiro
fundo_tabuleiro = pygame.image.load('img/fundo_tabuleiro.png')  # Substitua pelo caminho da imagem
fundo_tabuleiro = pygame.transform.scale(fundo_tabuleiro, (LARGURA, ALTURA))

# Carregando imagens dos personagens da Disney
mickey_image = pygame.image.load('img/minnie.png')  # Substitua 'mickey.png' pelo caminho para a imagem do Mickey Mouse
minnie_image = pygame.image.load('img/mickey.png')  # Substitua 'minnie.png' pelo caminho para a imagem da Minnie Mouse

# Redimensionando imagens para o tamanho do espaço no tabuleiro
mickey_image = pygame.transform.scale(mickey_image, (ESPACO, ESPACO))
minnie_image = pygame.transform.scale(minnie_image, (ESPACO, ESPACO))

# Sons
clique_som = pygame.mixer.Sound('img/clique.wav')  # Substitua 'clique.wav' pelo caminho para o efeito sonoro de clique
vitoria_som = pygame.mixer.Sound('img/vitoria.mp3')  # Substitua 'vitoria.wav' pelo caminho para o efeito sonoro de vitória

# Inicialização da Tela
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption('Jogo da Velha - Disney')
tela.fill(FUND0_COR)

# Tabuleiro (matriz 3x3) e vez do jogador
tabuleiro = [["" for _ in range(3)] for _ in range(3)]
vez_do_jogador = True  # True para jogador Mickey Mouse, False para Minnie Mouse
jogo_rodando = True
vencedor = None

# Pontuação dos jogadores
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
    input_box = pygame.Rect(50, 100, 200, 50)
    cor_fundo = pygame.Color('white')
    cor_texto = pygame.Color('black')
    nome = ""
    texto = ""

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
        input_text = fonte.render(nome, True, cor_texto)
        largura = max(200, input_text.get_width()+10)
        input_box.w = largura
        tela.blit(input_text, (input_box.x+5, input_box.y+5))
        pygame.draw.rect(tela, cor_fundo, input_box, 2)
        pygame.display.flip()

# Obter nomes dos jogadores
nome_jogador = obter_nome_jogador()
nome_ia = "Seu Zé"
# Função para adicionar botões gráficos
def adicionar_botoes():
    # Implemente botões gráficos para reiniciar, sair, regras, etc.
    pass

# Loop principal
while True:
    desenhar_tabuleiro()  # Certifique-se de que esta é a única chamada para desenhar_tabuleiro no loop principal
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
                    vencedor = nome_jogador  # Nome do jogador Mickey Mouse
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
        status_texto = STATUS_FONTE.render(f'Vez de: {"Mickey Mouse" if vez_do_jogador else "Minnie Mouse"}', True, (0, 0, 0))
        tela.blit(status_texto, (10, ALTURA - 30))
        

    pygame.display.update()

    if not vez_do_jogador and jogo_rodando:
        jogada_ia()
        clique_som.play()  # Reproduz som de clique
        if verificar_vitoria('O'):
            vitoria_som.play()  # Reproduz som de vitória
            vencedor = nome_ia  # Nome da Minnie Mouse
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
        pygame.time.wait(2000)  # Espera 2 segundos antes de reiniciar
        reiniciar()
