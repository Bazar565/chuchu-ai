import pygame
import random
import time
import math
import speech_recognition as sr
import threading
from gtts import gTTS
import os
from datetime import datetime
import cv2
import mediapipe as mp
import webbrowser
import requests
import json



mp_face_detection = mp.solutions.face_detection

# --- 1. CONFIGURAÇÕES INICIAIS ---
pygame.init()
pygame.mixer.init()

# Configurações da Tela (Fullscreen)
info = pygame.display.Info()
LARGURA, ALTURA = info.current_w, info.current_h
tela = pygame.display.set_mode((LARGURA, ALTURA), pygame.FULLSCREEN)
pygame.display.set_caption("Chuchu - Assistente Virtual")

# Cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERMELHO_BOCA = (200, 50, 50)
AZUL = (35, 35, 255)

# Proporções do Rosto (Calculadas dinamicamente)
centro_x, centro_y = LARGURA // 2, ALTURA // 2
distancia_olhos = LARGURA // 5
olho_y = ALTURA // 2
raio_olho = ALTURA // 4
raio_iris = int(raio_olho * 0.3)
raio_brilho = int(raio_iris * 0.2)

boca_y = int(ALTURA * 0.7)
largura_boca = LARGURA // 5
altura_boca = ALTURA // 30

# Variáveis de Estado Globais
olhar_x, olhar_y = 0, 0
ja_saudou = True
falando = False 
piscando = False
ultimo_rosto_visto = 0  

# Configuração do MediaPipe (Visão)
face_detection = mp_face_detection.FaceDetection(
    model_selection=0, 
    min_detection_confidence=0.5
)


# --- 2. SISTEMA DE VOZ ---
def falar_chuchu(texto):
    global falando
    arquivo_audio = "voz_chuchu.mp3"
    try:
        falando = True
        tts = gTTS(text=texto, lang='pt-br')
        tts.save(arquivo_audio)
        
        # --- ADICIONE ESTA PEQUENA ESPERA ---
        tentativas = 0
        while not os.path.exists(arquivo_audio) and tentativas < 10:
            time.sleep(0.1)
            tentativas += 1
        # ------------------------------------

        pygame.mixer.music.load(arquivo_audio)
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
            
        pygame.mixer.music.unload()
        
        
        if os.path.exists(arquivo_audio):
            os.remove(arquivo_audio)
            
    except Exception as e:
        print(f"Erro na voz: {e}")
    finally:
        falando = False

# --- 3. SISTEMA DE AUDIÇÃO ---
def tarefa_ouvir():
    reconhecedor = sr.Recognizer()
    # Calibra apenas UMA VEZ antes de entrar no loop infinito
    with sr.Microphone() as fonte:
        print("Calibrando silêncio inicial...")
        reconhecedor.adjust_for_ambient_noise(fonte, duration=1)

    while True:
        with sr.Microphone() as fonte:
            try:
                audio = reconhecedor.listen(fonte, timeout=None, phrase_time_limit=10)
                texto = reconhecedor.recognize_google(audio, language='pt-BR').lower()
                if "chuchu" in texto:
                    pygame.mixer.Sound("beep.wav").play()
                    print(texto)
                    time.sleep(1)
                    if any(p in texto for p in ["hora", "horas"]):
                        agora = datetime.now().strftime('%H:%M')
                        falar_chuchu(f"Agora são exatamente {agora}")

                    elif "soma" in texto or "quanto é" in texto:
                        numeros = [int(s) for s in texto.split() if s.isdigit()]
                        if len(numeros) >= 2:
                            falar_chuchu(f"A soma de {numeros[0]} mais {numeros[1]} é {sum(numeros)}")
                        else:
                            falar_chuchu("Desculpe, eu preciso de pelo menos dois números para somar.")

                    elif "abrir" in texto and "youtube" in texto:
                        falar_chuchu("Abrindo o painel do youtube para você.")
                        webbrowser.open("https://www.youtube.com.br")

                    elif "abrir" in texto and "google" in texto:
                        falar_chuchu("Abrindo o painel do Google para você.")
                        webbrowser.open("https://www.google.com.br")
            
                    elif "tchau" in texto or "fechar" in texto or "desligar" in texto:
                        falar_chuchu("Até logo!")
                        os._exit(0)
                    
                    elif "quem é" in texto or "você" in texto:
                        falar_chuchu("Eu sou a Chuchu, sua assistente virtual! Eu sei somar, sei a previsão do tempo, lembretes e as horas. em que posso ajudar?")
                    
                         # --- OPÇÃO 3: PREVISÃO DO TEMPO ---
                    elif "previsão do tempo" in texto or "como está o tempo" in texto:
                        # Aqui usamos a lógica do seu AlertaZap
                        # api_key = "9666deb35e0d08ac9c7fb8fe757c51ef"
                        cidade = "Caruaru"
                        link = "https://api.openweathermap.org/data/2.5/weather?q=Caruaru,BR&appid=9666deb35e0d08ac9c7fb8fe757c51ef&lang=pt_br"
                        requisicao = requests.get(link)
                        dados = requisicao.json()
                        temp = int(dados['main']['temp'] - 273.15)
                        desc = dados['weather'][0]['description']
                        umidade = dados["main"]["humidity"]
                        falar_chuchu(f"Previsão do tempo em {cidade}, faz {temp} graus, umidade relativa do ar {umidade} por cento, o céu está {desc} nesse momento!")

                         # Exemplo: "Chuchu, me lembre de tomar café às 15:00"
                         #elif "me lembre de" in texto and "às" in texto:
                    elif "me lembre de" in texto:
                         # Procuramos a posição da palavra "as" ou "às" para dividir a frase
                         # Usamos um split mais flexível para capturar o que vem depois de "me lembre de"
                        conteudo = texto.split("me lembre de ")[1]
                          # Tenta encontrar o divisor de horário (pode ser "as", "às" ou "as ")
                        divisor = " as " if " as " in conteudo else " às "
        
                        if divisor in conteudo:
                             parte_mensagem = conteudo.split(divisor)[0].strip()
                             parte_horario = conteudo.split(divisor)[1].strip()
            
                             falar_chuchu(f"Pois não! Vou te lembrar de {parte_mensagem} às {parte_horario}.")

                            # A FORMA CORRETA DE CHAMAR A THREAD:
                            # Passamos os argumentos dentro de 'args' para a thread não dar erro
                             threading.Thread(
                                  target=adicionar_alarme, 
                                  args=(parte_horario, parte_mensagem), 
                                  daemon=True
                              ).start()
                        else:
                             falar_chuchu("Você não me disse o horário do lembrete.")
                                  
            except sr.UnknownValueError:
                 # print("Não entendi o áudio")  # comente se quiser silêncio
                 pass  # não fala nada quando não entende
                
            except sr.RequestError:
                 falar_chuchu("Sem conexão com a internet.")

            except Exception as e:
                    print(f"Erro inesperado {e}")
                    falar_chuchu("Não entendi, pode repetir?")
               
          

# --- 4. SISTEMA DE VISÃO (RASTREAMENTO) ---
def tarefa_visao():

    global olhar_x, olhar_y, ja_saudou
    cap = cv2.VideoCapture(0)
    ultimo_rosto_visto = time.time()
    while True:
        ret, frame = cap.read()
        if not ret: break
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        resultado = face_detection.process(rgb_frame)
        if resultado.detections:
            for detection in resultado.detections:
                bboxC = detection.location_data.relative_bounding_box
                # Suavização do olhar (ajustado para 30 pixels de deslocamento)
                olhar_x = int((bboxC.xmin + bboxC.width/2 - 0.5) * 60)
                olhar_y = int((bboxC.ymin + bboxC.height/2 - 0.5) * 60)
                if not ja_saudou:
                    threading.Thread(target=falar_chuchu, args=("olá!",), daemon=True).start()
                    ja_saudou = False
        else:
            olhar_x, olhar_y = 0, 0
            if time.time() - ultimo_rosto_visto > 20:
               ja_saudou = True
        time.sleep(0.1)

# --- 5. FUNÇÕES DE DESENHO ---
def desenhar_olhos(esta_piscando):
    olho_esq_x = centro_x - distancia_olhos // 2
    olho_dir_x = centro_x + distancia_olhos // 2

    if esta_piscando:
        pygame.draw.line(tela, BRANCO, (olho_esq_x - raio_olho, olho_y), (olho_esq_x + raio_olho, olho_y), 10)
        pygame.draw.line(tela, BRANCO, (olho_dir_x - raio_olho, olho_y), (olho_dir_x + raio_olho, olho_y), 10)
    else:
        # Globos oculares
        pygame.draw.circle(tela, BRANCO, (olho_esq_x, olho_y), raio_olho)
        pygame.draw.circle(tela, BRANCO, (olho_dir_x, olho_y), raio_olho)

        # Íris (segue olhar_x e olhar_y)
        pygame.draw.circle(tela, AZUL, (olho_esq_x + olhar_x, olho_y + olhar_y), raio_iris)
        pygame.draw.circle(tela, AZUL, (olho_dir_x + olhar_x, olho_y + olhar_y), raio_iris)
        
        # Brilho
        offset = int(raio_iris * 0.4)
        pygame.draw.circle(tela, BRANCO, (olho_esq_x + olhar_x + offset, olho_y + olhar_y - offset), raio_brilho)
        pygame.draw.circle(tela, BRANCO, (olho_dir_x + olhar_x + offset, olho_y + olhar_y - offset), raio_brilho) # <-- se quiser voltar o brilho raio_brilho

#def desenhar_boca(esta_falando):
   
    # Centro e dimensões base
    #rect_boca = pygame.Rect(centro_x - largura_boca // 2, boca_y, largura_boca, altura_boca)
    
    #if esta_falando:
        # 1. Cria uma abertura que varia de forma orgânica
        # Usamos sin para o ritmo e random para a "sujeira" da fala real
        #ritmo = abs(math.sin(time.time() * 0)) 
        #variacao_fala = random.uniform(0.5, 1.1)
        #abertura_atual = int(altura_boca * 0 * ritmo * variacao_fala)
        
        # 2. Desenha a boca aberta (Elipse)
        # O Rect da boca aberta cresce para cima e para baixo
        #rect_aberta = pygame.Rect(
            #centro_x - largura_boca // 2, 
            #boca_y - (abertura_atual // 2), 
            #largura_boca, 
            #altura_boca + abertura_atual
        
        #)
        
        # Preenchimento e contorno
        #pygame.draw.ellipse(tela, VERMELHO_BOCA, rect_aberta)
        #pygame.draw.ellipse(tela, BRANCO, rect_aberta, 3)
        
        
    #else:
        # Boca fechada: Um sorriso sutil em arco
        # pi até 0 desenha a parte de baixo do círculo
        #pygame.draw.arc(tela, BRANCO, rect_boca, math.pi, 0, 3)
 
    
def agendar_previsao():
    print("Sincronizando relógio da Chuchu... 🛰️")
    
    while True:
        # Pega a hora atual
        agora = datetime.now()
        
        # Verifica se o minuto e o segundo são zero (ou seja, virada de hora)
        if agora.minute == 0 and agora.second == 0:
            # Aqui você chama a sua função que busca o tempo e faz ela falar
            #  Minha senha = "9666deb35e0d08ac9c7fb8fe757c51ef"
            cidade = "Caruaru"
            link = "https://api.openweathermap.org/data/2.5/weather?q=Caruaru,BR&appid=9666deb35e0d08ac9c7fb8fe757c51ef&lang=pt_br"
            try:
               requisicao = requests.get(link)
               dados = requisicao.json()
               temp = int(dados['main']['temp'] - 273.15)
               desc = dados['weather'][0]['description']
               umidade = dados["main"]["humidity"]
        
               falar_chuchu(f"Previsão do tempo em {cidade}, faz {temp} graus, umidade relativa do ar em {umidade} por cento, o céu está {desc} nesse momento!")
               falar_chuchu(f"Anunciando previsão das {agora.hour} horas.")
            except Exception as e:
                print(f"Erro ao buscar clima: {e}")
            # Dorme por 60 segundos para não repetir o anúncio no mesmo minuto
            time.sleep(60)
        # Verifica a cada 1 segundo para não perder o "pulo" da hora
        time.sleep(1)

        # --- AQUI É O LUGAR DA THREAD ---

# 2. Você dispara a "pista paralela" antes de começar o resto do seu programa
threading.Thread(target=agendar_previsao, daemon=True).start()

# 3. Daqui para baixo, o resto do seu código (reconhecimento de voz, gestos, etc)
print("Chuchu está operando e monitorando o relógio! 🚀")

# Função para carregar a agenda
def carregar_agenda():
    if not os.path.exists('agenda_chuchu.json'):
        return []
    try:
       with open('agenda_chuchu.json', 'r') as f:
        return json.load(f)
    except:
        return []    

# Função para salvar novo alarme
def adicionar_alarme(horario, mensagem):
    agenda = carregar_agenda()
    agenda.append({"horario": horario, "mensagem": mensagem, "tocado": False})
    with open('agenda_chuchu.json', 'w') as f:
        json.dump(agenda, f, indent=4, ensure_ascii=False)

# O "Cérebro" que checa o relógio
def verificar_alarmes():
    while True:
        agora = datetime.now().strftime("%H:%M")
        agenda = carregar_agenda()
        alterou = False

        for item in agenda:
            if item['horario'] == agora and not item['tocado']:
               falar_chuchu(f"Atenção, atenção ! São {agora} e você me pediu para lembrar: {item['mensagem']}")
               item['tocado'] = True
               alterou = True
    
        if alterou:
           with open('agenda_chuchu.json', 'w') as f:
               json.dump(agenda, f, indent=4, ensure_ascii=False)
        time.sleep(30)


# --- INICIALIZAÇÃO DAS THREADS ---
threading.Thread(target=tarefa_ouvir, daemon=True).start()
threading.Thread(target=tarefa_visao, daemon=True).start()
threading.Thread(target=verificar_alarmes, daemon=True).start()

# --- LOOP PRINCIPAL ---
ultimo_pisca = time.time()
clock = pygame.time.Clock()
rodando = True

while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
            rodando = False

    agora = time.time()
    tela.fill(PRETO)
    
    if agora - ultimo_pisca > random.uniform(3, 6) and not falando:
        piscando = True
        ultimo_pisca = agora
    if piscando and agora - ultimo_pisca > 0.15:
        piscando = False

    desenhar_olhos(piscando)
    #desenhar_boca(falando)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
