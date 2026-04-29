import pygame
import speech_recognition as sr
import threading
from gtts import gTTS
import os
import time
from datetime import datetime

# --- 1. INICIALIZAÇÃO ---
pygame.init()
pygame.mixer.init()

# Variável global para controlar a animação da boca na tela
falando = False 

def falar_chuchu(texto):
    """Faz a Chuchu falar usando a voz do Google (gTTS)"""
    global falando
    print(f"Chuchu diz: {texto}")
    
    arquivo_audio = "voz_chuchu.mp3"
    
    try:
        # Abre a boca na tela
        falando = True  
        
        # Gera o áudio com a voz do Google (Português do Brasil)
        # O 'lang=pt-br' garante que não haverá sotaque de inglês
        tts = gTTS(text=texto, lang='pt-br', slow=False)
        tts.save(arquivo_audio)
        
        # Carrega e toca o arquivo gerado
        pygame.mixer.music.load(arquivo_audio)
        pygame.mixer.music.play()
        
        # Mantém o código parado (e a boca aberta) enquanto o som toca
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        
        # Libera o arquivo para que ele possa ser sobrescrito na próxima fala
        pygame.mixer.music.unload()
        
        # Opcional: deleta o arquivo temporário para não acumular lixo
        if os.path.exists(arquivo_audio):
            os.remove(arquivo_audio)
            
    except Exception as e:
        print(f"Erro crítico na voz: {e}")
        # Se o Google falhar, a boca não pode ficar travada aberta
    
    finally:
        falando = False # Fecha a boca

# --- 2. LÓGICA DE AUDIÇÃO ---
def tarefa_ouvir():
    """Thread que fica ouvindo o microfone em segundo plano"""
    reconhecedor = sr.Recognizer()
    
    while True:
        with sr.Microphone() as fonte:
            # Ajusta para o barulho do ambiente do seu All-in-One
            reconhecedor.adjust_for_ambient_noise(fonte, duration=0.8)
            try:
                print("Aguardando você falar...")
                audio = reconhecedor.listen(fonte, timeout=None, phrase_time_limit=4)
                
                # Transforma áudio em texto
                texto = reconhecedor.recognize_google(audio, language='pt-BR').lower()
                print(f"Você disse: {texto}")

                # Comandos da Chuchu
                if "chuchu" in texto:
                    if "horas" in texto or "hora" in texto:
                        agora = datetime.now().strftime('%H:%M')
                        falar_chuchu(f"Agora são exatamente {agora}")
                    
                    elif "quem é você" in texto:
                        falar_chuchu("Eu sou a Chuchu, sua assistente virtual feita em Python!")
                    
                    elif "olá" in texto or "oi" in texto:
                        falar_chuchu("Olá! Como vai o trabalho no Bazar 55 hoje?")
                    
                    else:
                        falar_chuchu("Eu ouvi meu nome, mas não entendi o que você quer.")
            
            except sr.UnknownValueError:
                # Não entendeu nada, continua ouvindo em silêncio
                pass
            except Exception as e:
                print(f"Erro no microfone: {e}")

# --- 3. INICIALIZAÇÃO DA THREAD ---
# Isso permite que ela ouça enquanto o rosto (em outro arquivo) pisca
def iniciar_voz():
    thread_audio = threading.Thread(target=tarefa_ouvir, daemon=True)
    thread_audio.start()

# Teste rápido se rodar este arquivo sozinho
if __name__ == "__main__":
    iniciar_voz()
    falar_chuchu("Sistema de voz iniciado com sucesso.")
    # Mantém o script vivo para teste
    while True:
        time.sleep(1)
