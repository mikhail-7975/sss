import imutils
from imutils.video import VideoStream
from pyzbar import pyzbar
import argparse
import time
import cv2
# ВЫходные данные
# Создание и анализирование аргументов
ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", type=str, default="result.txt",)  # файл для записи
args = vars(ap.parse_args())
# Входные данные
# Запустите поток (запустите веб-камеру) и дайте датчику камеры прогреться.
print("Результат находится в файле result.txt")
vs = VideoStream(src=0).start()
# vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0)

# откройте исходящий CSV-файл для записи и инициализации
# штрих-коды (qr код), найденные до сих пор
csv = open(args["output"], "w")
#Множество в python - "контейнер", содержащий не повторяющиеся элементы в случайном порядке.
#Создаём множества:
found = set()


while True:
    # содержат максимальную ширину 400 пикселей.Изменяем размер изображения
    frame = vs.read()
    frame = imutils.resize(frame, width=400)

    # найдите штрих-коды (qr code) в таблице и расшифруйте каждый штрих-код.
    barcodes = pyzbar.decode(frame)

    # обнаружение баркода
    for barcode in barcodes:

        (x, y, w, h) = barcode.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2) # зеленая ограничительная рамка
#(изображение, начальная_точка, конечная_пункт, цвет, толщина)
        # преобразование штрих кода в строку
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type

        # рисует данные штрих-кода и тип штрих-кода на изображении.
        text = "{}".format(barcodeData)
        cv2.putText(frame, '', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        # текст вокруг qr code
        text = "{} ({})".format(barcodeData, barcodeType)
        cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)


        # csv.write("{},{}\n".format(datetime.datetime.now(), barcodeData)) #Дата снимка рядом с результатом

        if barcodeData not in found:


            csv.write("{}\n".format(barcodeData))
            csv.flush()

            found.clear()
            found.add(barcodeData)

    # Заголовок окна камеры
    cv2.imshow("Scanner", frame)
    key = cv2.waitKey(1) & 0xFF




# закрыть файл
print("[INFO] Completing the stream and closing the CSV file...")
csv.close()
cv2.destroyAllWindows()
vs.stop()