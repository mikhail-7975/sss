import cv2
import pyzbar.pyzbar as pyzbar
import serial as ser
import serial.tools.list_ports as ports_list


allowed_numbers = ['a1', 'a2', 'a3', 'a4']


def get_arduino_port():
    ports = list(ports_list.comports())

    for port in ports:
        if "Arduino" in port.description:
            return port.device

    return None


def send_to_serial(message: str):
    global serial

    serial.write(message.encode('utf-8'))


def get_cur_gray_frame():
    global video_capture

    ret, bgr_frame = video_capture.read()

    gray_frame = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2GRAY)

    return gray_frame


def analyze_qr(frame):
    decoded_objects = pyzbar.decode(frame)

    for decoded_object in decoded_objects:
        data = decoded_object.data.decode('utf-8')

        if data in allowed_numbers:
            send_to_serial('o')
        if data == 'to_close':
            send_to_serial('c')


def init():
    global serial, video_capture

    serial = ser.Serial(get_arduino_port())
    video_capture = cv2.VideoCapture(0)


def main():
    init()

    while 1:
        gray_frame = get_cur_gray_frame()

        cv2.imshow('frame', gray_frame)

        analyze_qr(gray_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == '__main__':
    main()