import pygame
import time
import math

# --- 1. CONFIGURAÇÕES E CORES ---
pygame.init()
info = pygame.display.Info()
LARGURA, ALTURA = info.current_w, info.current_h
tela = pygame.display.set_mode((LARGURA, ALTURA), pygame.FULLSCREEN)

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO_BOCA = (200, 50, 50)

# --- 2. VARIÁVEIS DE POSIÇÃO ---
centro_x = LARGURA // 2
boca_y = int(ALTURA * 0.7)
largura_boca = LARGURA // 5
altura_boca = ALTURA // 15

# Simulação do estado da Chuchu (mude para True para ver o movimento)
falando = True 

# --- 3. FUNÇÃO DE MOVIMENTO DA BOCA ---
def desenhar_movimento_boca(esta_falando):
    # Definimos um retângulo único para garantir que um desenho fique exatamente sobre o outro
    # O ajuste de +40 na altura é para o oval ter espaço para aparecer bem
    retangulo_boca = pygame.Rect(centro_x - largura_boca // 2, boca_y - 20, largura_boca, altura_boca + 40)
    
    if esta_falando:
        # Lógica de tempo: muda o estado apenas na virada do segundo (0, 1, 2, 3...)
        # % 2 == 0 alterna entre Par (Verdadeiro) e Ímpar (Falso) a cada 1 segundo
        if int(time.time() * 4) % 2 == 0:
            # ESTADO A: Círculo Oval Vermelho
            pygame.draw.ellipse(tela, VERMELHO_BOCA, retangulo_boca)
            pygame.draw.ellipse(tela, BRANCO, retangulo_boca, 3) # Contorno branco
        else:
            # ESTADO B: Arco Simpático (Sobreposto no mesmo lugar)
            # O arco é desenhado na metade inferior do retângulo (math.pi até 0)
            pygame.draw.arc(tela, BRANCO, retangulo_boca, math.pi, 0, 6)
    else:
        # ESTADO REPOUSO: Apenas o arco parado
        pygame.draw.arc(tela, BRANCO, retangulo_boca, math.pi, 0, 6)

# --- 4. LOOP DE EXECUÇÃO ---
rodando = True
relogio = pygame.time.Clock()

while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
            rodando = False

    # Limpa o fundo
    tela.fill(PRETO)

    # Chama a função de movimento
    desenhar_movimento_boca(falando)

    # Atualiza a tela
    pygame.display.flip()
    relogio.tick(60) # Mantém 60 FPS para suavidade, mas a boca só muda a 1Hz

pygame.quit()
