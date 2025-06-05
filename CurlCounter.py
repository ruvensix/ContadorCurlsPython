import cv2
import mediapipe as mp
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Função para calcular o ângulo entre três pontos
def calculate_angle(a, b, c):
    a = np.array(a)  # Primeiro ponto
    b = np.array(b)  # Ponto do meio (vértice)
    c = np.array(c)  # Último ponto

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle


cap = cv2.VideoCapture(0)  # Abre a câmara (0 é a câmara padrão)

# Variáveis do contador de curls
counter = 0  # Inicializa o contador
stage = None  # Inicializa a fase do curl ("cima" ou "baixo")

# Configuração do Mediapipe Pose
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():  # Loop principal: enquanto a câmara estiver aberta
        ret, frame = cap.read()  # Lê um frame da câmara

        # Converter a imagem de BGR (OpenCV) para RGB (Mediapipe)
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False  # Desativa a flag de escrita para otimização

        # Detecção da pose
        results = pose.process(image)  # Processa a imagem com o Mediapipe

        # Converter de volta para BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Extrair os landmarks (pontos de referência da pose)
        try:
            landmarks = results.pose_landmarks.landmark  # Obtém os landmarks detectados

            # Obter coordenadas dos pontos relevantes (ombro, cotovelo, pulso)
            shoulder = [
                landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y,
            ]
            elbow = [
                landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y,
            ]
            wrist = [
                landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y,
            ]

            # Calcular o ângulo do cotovelo
            angle = calculate_angle(shoulder, elbow, wrist)

            # Exibir o ângulo na imagem (perto do cotovelo)
            h, w, c = image.shape  # Obtém as dimensões da imagem
            cv2.putText(
                image,
                str(int(angle)),  # Converte o ângulo para string
                tuple(
                    np.multiply(elbow, [w, h]).astype(
                        int
                    )
                ),  # Posição do texto (coordenadas do cotovelo)
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 255, 255),
                2,
                cv2.LINE_AA,
            )

            # Lógica do contador de curls
            if angle > 160:  # Braço esticado (fase "baixo")
                stage = "Baixo"
            if angle < 30 and stage == "Baixo":  # Braço dobrado (fase "cima")
                stage = "Cima"
                counter += 1  # Incrementa o contador
                print(counter)  # Exibe a contagem no terminal

        except:
            pass  # Se não detectar a pose, ignora

        # --- Renderizar a caixa de contagem e texto ---
        # Desenha um retângulo para o fundo da informação
        cv2.rectangle(image, (0, 0), (225, 73), (245, 117, 16), -1)  # Canto superior esquerdo

        # Dados das Repetições (REPS)
        cv2.putText(
            image,
            "REPS",  # Texto
            (15, 12),  # Posição
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 0, 0),
            1,
            cv2.LINE_AA,
        )
        cv2.putText(
            image,
            str(counter),  # Valor da contagem
            (10, 60),  # Posição
            cv2.FONT_HERSHEY_SIMPLEX,
            2,
            (255, 255, 255),
            2,
            cv2.LINE_AA,
        )

        # Dados da Fase (STAGE)
        cv2.putText(
            image,
            "FASE",  # Texto
            (120, 12),  # Posição (ajustado para não sobrepor REPS)
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 0, 0),
            1,
            cv2.LINE_AA,
        )
        cv2.putText(
            image,
            str(stage),  # Valor da fase
            (115, 60),  # Posição (ajustado)
            cv2.FONT_HERSHEY_SIMPLEX,
            2,
            (255, 255, 255),
            2,
            cv2.LINE_AA,
        )

        # Desenha os landmarks (esqueleto) na imagem
        mp_drawing.draw_landmarks(
            image,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
            mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2),
        )

        cv2.imshow("Mediapipe Feed", image)  # Mostra a imagem na janela

        if cv2.waitKey(10) & 0xFF == ord(
            "q"
        ):  # Espera 10ms por uma tecla 'q' para sair
            break

    cap.release()  # Libera a câmara
    cv2.destroyAllWindows()  # Fecha todas as janelas