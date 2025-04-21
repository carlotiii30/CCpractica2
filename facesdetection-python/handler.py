import cv2
import numpy as np
import urllib.request
from flask import request, Response


def handle(req=None):
    try:
        image_url = request.get_data(as_text=True).strip()
        print(f"URL recibida: {image_url}")

        resp = urllib.request.urlopen(image_url)
        image_np = np.asarray(bytearray(resp.read()), dtype="uint8")
        img = cv2.imdecode(image_np, cv2.IMREAD_COLOR)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        for x, y, w, h in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

        _, buffer = cv2.imencode(".jpg", img)
        img_bytes = buffer.tobytes()

        return Response(img_bytes, content_type="image/jpeg")

    except Exception as e:
        return Response(
            f"Error procesando la imagen: {str(e)}",
            status=500,
            content_type="text/plain",
        )
