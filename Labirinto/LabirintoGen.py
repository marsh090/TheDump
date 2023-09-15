import random
import numpy as np
import pygame
import time

# Constantes para direções
CIMA = 1
BAIXO = 2
ESQUERDA = 3
DIREITA = 4

# Cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)

def tela_inicial():
    pygame.init()
    tela = pygame.display.set_mode((400, 200))
    pygame.display.set_caption('Escolha o Tamanho do Labirinto')
    clock = pygame.time.Clock()
    
    fonte = pygame.font.Font(None, 24)  # Fonte padrão, tamanho 36
    
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return None

        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        # Desenha botões e verifica cliques
        botoes = [(50, 50, "Pequeno", 22), (150, 50, "Médio", 56), (250, 50, "Grande", 100)]
        for x, y, texto, tamanho in botoes:
            pygame.draw.rect(tela, VERDE, (x, y, 80, 40))
            
            texto_superficie = fonte.render(texto, True, (0, 0, 0))  # Texto, anti-aliasing, cor
            texto_rect = texto_superficie.get_rect(center=(x + 40, y + 20))  # Centraliza o texto no botão
            tela.blit(texto_superficie, texto_rect)
            
            if x < mouse_pos[0] < x + 80 and y < mouse_pos[1] < y + 40:
                if mouse_click[0]:
                    return tamanho

        pygame.display.flip()
        clock.tick(60)

# Classe que define o labirinto
class Labirinto:
    def __init__(self, tamanho, inicio, fim):
        self.tamanho = tamanho
        self.inicio = inicio
        self.fim = fim
        self.labirinto = np.zeros((tamanho, tamanho), dtype=int)
        self.labirinto[inicio[0]][inicio[1]] = 1
        self.labirinto[fim[0]][fim[1]] = 1

    def geraLabirinto(self):
        random.seed(time.time())
        self.labirinto = np.zeros((self.tamanho, self.tamanho), dtype=int)
        self.labirinto[self.inicio[0]][self.inicio[1]] = 1
        posicao = self.inicio.copy()
        pilha = [posicao]
        self.labirinto[self.fim[0]][self.fim[1]] = 0  # Garante que o fim seja uma parede inicialmente

        while pilha:
            x, y = posicao
            direcoes = []

            if x > 1 and self.labirinto[x-2][y] == 0:
                direcoes.append(CIMA)
            if x < self.tamanho - 2 and self.labirinto[x+2][y] == 0:
                direcoes.append(BAIXO)
            if y > 1 and self.labirinto[x][y-2] == 0:
                direcoes.append(ESQUERDA)
            if y < self.tamanho - 2 and self.labirinto[x][y+2] == 0:
                direcoes.append(DIREITA)

            if direcoes:
                direcao = random.choice(direcoes)

                if direcao == CIMA:
                    self.labirinto[x-1][y] = self.labirinto[x-2][y] = 1
                    posicao = [x-2, y]
                elif direcao == BAIXO:
                    self.labirinto[x+1][y] = self.labirinto[x+2][y] = 1
                    posicao = [x+2, y]
                elif direcao == ESQUERDA:
                    self.labirinto[x][y-1] = self.labirinto[x][y-2] = 1
                    posicao = [x, y-2]
                elif direcao == DIREITA:
                    self.labirinto[x][y+1] = self.labirinto[x][y+2] = 1
                    posicao = [x, y+2]

                pilha.append(posicao.copy())
            else:
                posicao = pilha.pop()

        self.labirinto[self.fim[0]][self.fim[1]] = 1  # Garante que o fim seja alcançável

    def desenhaLabirinto(self):
        pygame.init()
        tela = pygame.display.set_mode((self.tamanho * 10 + 20, self.tamanho * 10 + 20))
        pygame.display.set_caption('Labirinto')
        clock = pygame.time.Clock()

        while True:
            jogador = self.inicio.copy()
            rodando = True
            while rodando:
                for evento in pygame.event.get():
                    if evento.type == pygame.QUIT:
                        pygame.quit()
                        return

                keys = pygame.key.get_pressed()

                if keys[pygame.K_LEFT]:
                    if self.labirinto[jogador[0]][jogador[1] - 1] == 1:
                        jogador[1] -= 1
                if keys[pygame.K_RIGHT]:
                    if self.labirinto[jogador[0]][jogador[1] + 1] == 1:
                        jogador[1] += 1
                if keys[pygame.K_UP]:
                    if self.labirinto[jogador[0] - 1][jogador[1]] == 1:
                        jogador[0] -= 1
                if keys[pygame.K_DOWN]:
                    if self.labirinto[jogador[0] + 1][jogador[1]] == 1:
                        jogador[0] += 1

                if jogador == self.fim:
                    self.geraLabirinto()
                    break

                tela.fill(PRETO)

                for i in range(self.tamanho):
                    for j in range(self.tamanho):
                        cor = BRANCO if self.labirinto[i][j] == 1 else PRETO
                        pygame.draw.rect(tela, cor, (j * 10 + 10, i * 10 + 10, 10, 10))

                pygame.draw.rect(tela, VERMELHO, (jogador[1] * 10 + 10, jogador[0] * 10 + 10, 10, 10))
                pygame.draw.rect(tela, VERDE, (self.fim[1] * 10 + 10, self.fim[0] * 10 + 10, 10, 10))

                pygame.display.flip()
                clock.tick(60)

if __name__ == "__main__":
    tamanho_escolhido = tela_inicial()
    if tamanho_escolhido is not None:
        inicio = [0, 0]
        fim = [tamanho_escolhido - 2, tamanho_escolhido - 2]
        labirinto = Labirinto(tamanho_escolhido, inicio,  fim)
        labirinto.geraLabirinto()
        labirinto.desenhaLabirinto()
