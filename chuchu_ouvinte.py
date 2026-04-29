import speech_recognition as sr

def ouvir_chuchu():
    # Cria o reconhecedor
    reconhecedor = sr.Recognizer()
    
    with sr.Microphone() as fonte:
        # Ajusta o ruído ambiente (importante para não confundir a Chuchu)
        reconhecedor.adjust_for_ambient_noise(fonte, duration=1)
        print("Chuchu está ouvindo... (Diga algo!)")
        
        try:
            # Captura o áudio
            audio = reconhecedor.listen(fonte, timeout=5)
            
            # Reconhece usando o Google (em português)
            texto = reconhecedor.recognize_google(audio, language='pt-BR')
            print(f"Você disse: {texto}")
            return texto.lower()
            
        except sr.UnknownValueError:
            print("Chuchu não entendeu o que você disse.")
            return None
        except sr.RequestError:
            print("Erro de conexão com o serviço de voz.")
            return None
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            return None

# Teste simples
if __name__ == "__main__":
    ouvir_chuchu()
