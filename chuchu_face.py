import pygame
import random
import time
import math

# Inicialização do Pygame
pygame.init()

# Configurações da Tela (Pega a resolução do seu All-in-One)
info = pygame.display.Info()
# Use FULLSCREEN para o All-in-One, ou tire para testar em janela
LARGURA, ALTURA = info.current_w, info.current_h
tela = pygame.display.set_mode((LARGURA, ALTURA), pygame.FULLSCREEN) 
# tela = pygame.display.set_mode((1280, 720)) # Descomente para testar em janela menor
pygame.display.set_caption("Chuchu - Assistente Virtual")

# Cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERMELHO_BOCA = (200, 50, 50) # Um vermelho mais suave para a boca

# Configurações do Rosto (Ajustado para telas grandes de All-in-One)
olho_y = ALTURA // 3 * 1.2 # Olhos um pouco acima do centro
raio_olho = ALTURA // 10 # Tamanho proporcional à altura da tela
distancia_olhos = LARGURA // 4 # Separação dos olhos


# --- NOVA CONFIGURAÇÃO DA ÍRIS ---
# A íris terá 60% do tamanho do olho branco (ajuste se quiser maior ou menor)
raio_iris = int(raio_olho * 0.6)



boca_y = ALTURA // 3 * 2 # Boca abaixo do centro
largura_boca = LARGURA // 5
altura_boca = ALTURA // 15

def desenhar_olhos(piscando):
    # Posição x dos olhos
    olho_esq_x = (LARGURA // 2) - distancia_olhos // 2
    olho_dir_x = (LARGURA // 2) + distancia_olhos // 2
    
    if piscando:
        # Se estiver piscando, desenha apenas um risco espesso (olho fechado)
        espessura_pisco = raio_olho // 4
        pygame.draw.line(tela, BRANCO, (olho_esq_x - raio_olho, olho_y), (olho_esq_x + raio_olho, olho_y), espessura_pisco)
        pygame.draw.line(tela, BRANCO, (olho_dir_x - raio_olho, olho_y), (olho_dir_x + raio_olho, olho_y), espessura_pisco)
    else:
        # --- PASSO 1: Olho aberto (Círculos BRANCOS grandes) ---
        pygame.draw.circle(tela, BRANCO, (olho_esq_x, olho_y), raio_olho)
        pygame.draw.circle(tela, BRANCO, (olho_dir_x, olho_y), raio_olho)
        
        # --- PASSO 2: A Íris (Círculos PRETO menores dentro do branco) ---
        # Elas ficam centralizadas no mesmo ponto (olho_y)
        pygame.draw.circle(tela, PRETO, (olho_esq_x, olho_y), raio_iris)
        pygame.draw.circle(tela, PRETO, (olho_dir_x, olho_y), raio_iris)
        
        # --- OPCIONAL: Destaque de Luz (Pupila) ---
        # Se quiser dar ainda mais vida, podemos adicionar um pontinho branco bem pequeno
        # deslocado para o canto superior direito da íris (simula o reflexo da luz ambiente).
        raio_pupila = int(raio_iris * 0.2)
        pygame.draw.circle(tela, BRANCO, (olho_esq_x + raio_iris//2, olho_y - raio_iris//2), raio_pupila)
        pygame.draw.circle(tela, BRANCO, (olho_dir_x + raio_iris//2, olho_y - raio_iris//2), raio_pupila)


def desenhar_boca(falando=False):
    # Retângulo que define a área da boca (para o arco)
    rect_boca = pygame.Rect(LARGURA // 2 - largura_boca // 2, boca_y, largura_boca, altura_boca)
    
    # Desenha um sorriso simples (um arco para baixo)
    # pygame.draw.arc(superfície, cor, retângulo, ângulo_inicial, ângulo_final, espessura)
    # Os ângulos são em radianos. math.pi é 180 graus.
    angulo_inicio = math.pi # Começa no "oeste" (pi)
    angulo_fim = 0 # Termina no "leste" (0)
    
    if falando:
        # Se estiver falando, fazemos a boca abrir um pouco (um círculo oval)
        if falando:
           pygame.draw.ellipse(tela, VERMELHO_BOCA, rect_boca)
           pygame.draw.ellipse(tela, BRANCO, rect_boca, 3) # Contorno branco para destacar no fundo preto
        
        # pygame.draw.ellipse(tela, VERMELHO_BOCA, rect_boca)
        # pygame.draw.ellipse(tela, PRETO, rect_boca, 5) # Contorno
    else:
        # Boca normal: um sorriso suave
        pygame.draw.arc(tela, VERMELHO_BOCA, rect_boca, angulo_inicio, angulo_fim, 15)
        # Opcional: desenhar a linha preta do sorriso por cima
        pygame.draw.arc(tela, PRETO, rect_boca, angulo_inicio, angulo_fim, 5)

# Loop Principal
rodando = True
piscando = False
falando = False # Variável para controlar a animação da boca futuramente
ultimo_pisca = time.time()
tempo_proximo_pisca = random.uniform(3, 6) # Pisca a cada 3 a 6 segundos

clock = pygame.time.Clock() # Para controlar o FPS

while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE: # Aperte ESC para fechar
                rodando = False
            # Teste rápido: aperte 'F' para simular que ela está falando
            if evento.key == pygame.K_f:
                falando = not falando

    agora = time.time()
    
    # Limpa a tela com fundo branco
    tela.fill(PRETO)
    
    # Lógica para piscar
    if agora - ultimo_pisca > tempo_proximo_pisca and not falando: # Não pisca enquanto fala
        piscando = True
        desenhar_olhos(piscando)
        desenhar_boca(falando)
        pygame.display.flip()
        time.sleep(0.12) # Tempo do olho fechado (um pouco mais rápido)
        piscando = False
        ultimo_pisca = agora
        tempo_proximo_pisca = random.uniform(4, 8) # Próximo pisco demorará mais

    # Desenha o rosto completo
    desenhar_olhos(piscando)
    desenhar_boca(falando)
    
    # Atualiza a tela
    pygame.display.flip()
    
    # Limita a 60 quadros por segundo para não sobrecarregar a CPU
    clock.tick(60)

pygame.quit()
