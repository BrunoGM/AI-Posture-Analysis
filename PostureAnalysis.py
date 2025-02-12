import cv2
import mediapipe as mp
import math
import time
import numpy as np
import matplotlib.pyplot as plt
import winsound

# Inicializa a classe de pose do mediapipe
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

def calcular_altura(a, b, c):
    numerador = abs((b.y - a.y) * c.x - (b.x - a.x) * c.y + b.x * a.y - b.y * a.x)
    denominador = math.sqrt((b.y - a.y)**2 + (b.x - a.x)**2)
    altura = numerador / denominador
    return altura

def calcular_distancia(a, b):
    return math.sqrt((b.x - a.x) ** 2 + (b.y - a.y) ** 2)

# Limiares para avaliação da postura
THRESHOLD_BOA_POSTURA = 0.95
THRESHOLD_POSTURA_MEDIA = 0.85
THRESHOLD_ALERTA_TEMPO = 3
FREQUENCIA_BEEP = 1000
DURACAO_BEEP = 500

# Abre a webcam
cap = cv2.VideoCapture(0)

# Variáveis para calibração
altura_calibrada = None
modo_calibracao = False
iniciar_gravacao = False

# Variáveis para análise temporal e plotagem
dados_postura = []
marcas_tempo = []
status_postura = []
tempo_inicio_ma_postura = None

try:
    while True:
        ret, frame = cap.read()
        
        if not ret:
            print("Falha ao capturar frame")
            break

        frame = cv2.flip(frame, 1)
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
            
            ombro_esquerdo = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
            ombro_direito = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
            nariz = landmarks[mp_pose.PoseLandmark.NOSE.value]

            altura_imagem, largura_imagem, _ = image.shape
            ombro_esquerdo_pixel = (int(ombro_esquerdo.x * largura_imagem), int(ombro_esquerdo.y * altura_imagem))
            ombro_direito_pixel = (int(ombro_direito.x * largura_imagem), int(ombro_direito.y * altura_imagem))
            nariz_pixel = (int(nariz.x * largura_imagem), int(nariz.y * altura_imagem))

            cv2.line(image, ombro_esquerdo_pixel, ombro_direito_pixel, (0, 255, 0), 2)
            cv2.line(image, nariz_pixel, ((ombro_esquerdo_pixel[0] + ombro_direito_pixel[0]) // 2, 
                    (ombro_esquerdo_pixel[1] + ombro_direito_pixel[1]) // 2), (255, 0, 0), 2)

            altura_triangulo = calcular_altura(ombro_esquerdo, ombro_direito, nariz)
            largura_ombros = calcular_distancia(ombro_esquerdo, ombro_direito)
            
            if largura_ombros > 0:
                altura_normalizada = altura_triangulo / largura_ombros
            else:
                altura_normalizada = 0

            if modo_calibracao:
                altura_calibrada = altura_normalizada
                modo_calibracao = False
                iniciar_gravacao = True
                dados_postura = []
                marcas_tempo = []
                status_postura = []
                tempo_inicio_sessao = time.time()
                cv2.putText(image, "Calibracao Completa", (50, 100), 
                          cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            if iniciar_gravacao:
                tempo_atual = time.time() - tempo_inicio_sessao
                dados_postura.append(altura_normalizada)
                marcas_tempo.append(tempo_atual)
                
                if altura_calibrada > 0:
                    razao_altura = altura_normalizada / altura_calibrada
                    if razao_altura >= THRESHOLD_BOA_POSTURA:
                        status_postura_atual = "Boa Postura"
                        cor_postura = (0, 255, 0)
                    elif razao_altura >= THRESHOLD_POSTURA_MEDIA:
                        status_postura_atual = "Postura Media"
                        cor_postura = (0, 255, 255)
                    else:
                        status_postura_atual = "Ma Postura"
                        cor_postura = (0, 0, 255)
                else:
                    status_postura_atual = "Desconhecido"
                    cor_postura = (255, 255, 255)

                cv2.putText(image, f"{status_postura_atual}", 
                            (10, 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, cor_postura, 2)
                
                status_postura.append(status_postura_atual)

                cv2.putText(image, f"Altura: {altura_normalizada:.2f}", 
                          (10, 30),
                          cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

                if status_postura_atual == "Ma Postura":
                    if tempo_inicio_ma_postura is None:
                        tempo_inicio_ma_postura = time.time()
                    elif time.time() - tempo_inicio_ma_postura >= THRESHOLD_ALERTA_TEMPO:
                        winsound.Beep(FREQUENCIA_BEEP, DURACAO_BEEP)
                        tempo_inicio_ma_postura = time.time()
                else:
                    tempo_inicio_ma_postura = None

            else:
                cv2.putText(image, "Pressione 'c' para calibrar", (50, 50), 
                          cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

        cv2.imshow('Analise de Postura', image)

        key = cv2.waitKey(10) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('c'):
            modo_calibracao = True

finally:
    if len(dados_postura) > 0:
        plt.figure(figsize=(12, 6))
        plt.plot(marcas_tempo, dados_postura, 'b-', label='Altura Normalizada', linewidth=2)
        if altura_calibrada is not None:
            plt.axhline(y=altura_calibrada, color='y', linestyle='-', label='Altura Calibrada')
        plt.xlabel('Tempo (segundos)')
        plt.ylabel('Altura Normalizada')
        plt.title('Variação da Postura ao Longo do Tempo')
        plt.legend()
        plt.grid(True)
        plt.show()

        tempo_total = marcas_tempo[-1] - marcas_tempo[0]
        total_frames = len(status_postura)
        contagem_boa = status_postura.count("Boa Postura")
        contagem_media = status_postura.count("Postura Media")
        contagem_ma = status_postura.count("Ma Postura")

        porcentagem_boa = (contagem_boa / total_frames) * 100
        porcentagem_media = (contagem_media / total_frames) * 100
        porcentagem_ma = (contagem_ma / total_frames) * 100

        print("\nResumo da Análise de Postura:")
        print(f"Tempo Total Gravado: {tempo_total:.2f} segundos")
        print(f"Boa Postura: {porcentagem_boa:.2f}%")
        print(f"Postura Media: {porcentagem_media:.2f}%")
        print(f"Ma Postura: {porcentagem_ma:.2f}%")

    cap.release()
    cv2.destroyAllWindows()