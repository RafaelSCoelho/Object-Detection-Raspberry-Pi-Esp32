import cv2
import socket
import threading
import numpy as np
from urllib.request import urlopen
import send_email
import imports
import camera

porcentage = 0
HEADER = 64
codificacao = "utf-8"
thres = 0.45
classNames = [],
datas = {}

Conexao_Socket = ("IP", 5050)
Server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Server.bind(Conexao_Socket)

def create_alert_message(porcentage):
    with open("message_alert", "w") as file:
        file.write("!!!!! HIGH ALERT !!!!!!\n")
        file.write(f"Was detected someone armed {porcentage}% \n")
        file.close()

def handle_client(conn, addr):
    porcentage = 0
    url = "http://" + addr[0] + ":81"
    print("[Host] {} connectado".format(addr))
    connected = True
    while connected:
        capt = camera.video_stream(url)
        image = Object_Detector(capt)
        cv2.imshow('image', image[0])
        cv2.waitKey(1)
        id_esp = threading.activeCount() - 1
        con = id_esp, addr[1]
        print(id_esp)
        datas[con] = image[1]
        if datas.get(con):
            datas[con] = image[1]
            porcentage = sum(list(datas.values()))
        final_test = porcentage / id_esp
        print(f"Con{id_esp, addr[1]} Porcentage: {image[1]}")
        if final_test >= thres:
            print(f"[{final_test * 100:.2f} %] Armas encontrada")
            target_email = send_email.email_alert(capt)
            print(f"Email is send")
    conn.close()

def Object_Detector(img):
    classIds, confs, bbox = net.detect(img, confThreshold=thres)
    confidence = 0
    if len(classIds) != 0:
        for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):
            cv2.rectangle(img, box, color=(0, 255, 0), thickness=2)
            cv2.putText(img, classNames[classId - 1].upper(), (box[0] + 10, box[1] + 30),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2, )
            cv2.putText(img, str(round(confidence * 100, 2)), (box[0] + 200, box[1] + 30),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2, )
    return img, confidence

def start():
    Server.listen()
    print("[LISTENING] Servidor {}".format("192.168.1.7"))
    while True:
        conn, addr = Server.accept()
        create_alert_message(porcentage)

        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        Qtd_host = threading.activeCount() - 1
        print("[Host Conectados] {}".format(Qtd_host))


if __name__ == "__main__":
    print("[STARTING] Servidor Iniciado ...")
    start()
