import cv2
import numpy as np

video_path = "C:\\Users\\caco2\\Desktop\\Sin título.mp4"
cap = cv2.VideoCapture(video_path)

# Definir las nuevas dimensiones deseadas para el video
new_dimensions = (1000, 700)

# Definir la posición deseada de los parches
desired_position = (150, 150)

# Inicializar variables de seguimiento
object_detected = False
object_crossed = False
counter = 0

while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        break

    # Redimensionar el frame a las nuevas dimensiones
    frame = cv2.resize(frame, new_dimensions)
    # Convertir el frame a formato HSV
    imghsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Definir rango de color amarillo en formato HSV
    amarillobajo = np.array([20, 50, 50], np.uint8)
    amarilloalto = np.array([32, 255, 255], np.uint8)

    # Crear una máscara para objetos amarillos
    mask_amarillo = cv2.inRange(imghsv, amarillobajo, amarilloalto)

    # Definir rango de color verde en formato HSV
    verdebajo = np.array([36, 50, 50], np.uint8)
    verdealto = np.array([75, 255, 255], np.uint8)
    
    # Crear una máscara para objetos verdes
    mask_verde = cv2.inRange(imghsv, verdebajo, verdealto)

    # Combinar las máscaras para detectar objetos amarillos y verdes
    mask = cv2.bitwise_or(mask_amarillo, mask_verde)

    # Encontrar contornos en la máscara combinada
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Iterar a través de los contornos y verificar la posición deseada
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)

        # Dibujar rectángulo alrededor del objeto
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Calcular el centro del rectángulo delimitador
        center_x = x + w // 2
        center_y = y + h // 2

        if (
            desired_position[0] < center_x < desired_position[0] + 50
            and desired_position[1] < center_y < desired_position[1] + 50
        ):
            if np.any(mask_amarillo[y:y+h, x:x+w]) or np.any(mask_verde[y:y+h, x:x+w]):
                if not object_detected:
                    object_detected = True
            else:
                object_detected = False

    # Verificar si el objeto cruza la posición deseada
    if object_detected and not object_crossed:
        counter += 1
        object_crossed = True
    elif not object_detected:
        object_crossed = False
    cv2.putText(frame, f"Crossings: {counter}", (10, 30), cv2.FONT_HERSHEY_DUPLEX, 1.5, (0, 0, 0), 2)
    cv2.imshow('Detected Objects', frame)


    if cv2.waitKey(25) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
