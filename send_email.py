import imghdr
import smtplib
from sendemail.message import EmailMessage
import cv2

def email_alert(image):
    cv2.imwrite("C:/Users/rafa_/PycharmProjects/TCC/image.jpg", image)
    cap = cv2.VideoCapture("image.jpg")
    success, frame = cap.read()

    with open(frame, 'rb') as fp:
        img_data = fp.read()

    with open("message_alert", 'r') as g:
        msg = EmailMessage()
        msg.get_content(g.read())

    msg.add_attachment(img_data, maintype='image', subtype=imghdr.what(None, img_data))
    send_email = "rafael.santana@unemat.br"
    target_email = "rafa_coelho4@hotmail.com"
    msg['Subject'] = f'!!!!!!!!-ALERT-!!!!!!!!'
    msg['From'] = send_email
    msg['To'] = target_email
    msg.preamble = 'You will not see this in a MIME-aware mail reader.\n'

    with smtplib.SMTP('localhost') as s:
        s.send_message(msg)

    return target_email