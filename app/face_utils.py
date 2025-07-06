import base64
import numpy as np
import cv2
import face_recognition

def get_face_encoding_from_base64(imagem_base64: str):
    # Decodifica base64 para bytes
    img_bytes = base64.b64decode(imagem_base64)
    # Converte bytes para numpy array
    nparr = np.frombuffer(img_bytes, np.uint8)
    # Decodifica imagem
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    # Extrai encoding facial
    encodings = face_recognition.face_encodings(img)
    if encodings:
        return encodings[0].tolist()  # Converte para lista para salvar como JSON
    return None 