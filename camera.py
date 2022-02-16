
import cv2 as cv
import numpy as np
from urllib.request import urlopen

def video_stream(url):
    buffer_camera = 4096
    stream = urlopen(url)
    bytes = b''
    i = 0
    while True:
        bytes += stream.read(buffer_camera)
        jpg_inicio = bytes.find(b'\xff\xd8')
        jpg_fim = bytes.find(b'\xff\xd9')
        if jpg_inicio >- 1 and jpg_fim >- 1:
            jpg = bytes[jpg_inicio:jpg_fim+2]
            bytes = bytes[jpg_fim+2:]
            image = cv.imdecode(np.frombuffer(jpg,dtype=np.uint8),cv.IMREAD_UNCHANGED)
            image = cv.resize(image, (800, 600))
            return image

if __name__ == "__main__":
    url = "http://192.168.0.106:81"
    while True:
        capt = video_stream(url)
        cv.imwrite("/home/rafael/PycharmProjects/Yolov3Project/frames.jpg", capt)
        cap = cv.VideoCapture("frames.jpg")
        success, frame = cap.read()
        #result = Object_Detector(frame)
        cv.imshow("Output", frame)
        cv.waitKey(1)
    cap.release()
    cv.destroyAllWindows()

