import cv2
import pyzbar.pyzbar as pyzbar
import serial
ser = serial.Serial()#вставить name в ()
cap = cv2.VideoCapture(0)#захват камеры
font = cv2.FONT_HERSHEY_PLAIN#размер текста
value = b'c'
ser.write(value)#отправка value на ком.порт
while True:
    rat, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    decodedObjects = pyzbar.decode(gray)
    for obj in decodedObjects:
        cv2.putText(gray, str(obj.data), (50, 50), font, 2, (255, 0, 0), 2)
        if str(obj.data) == "b\'Open\'":
            value = b'o'
            ser.write(value)
        elif str(obj.data) == "b\'Close\'":
            value = b'c'
            ser.write(value)
    cv2.imshow("Frame", gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break