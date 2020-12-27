from imutils.video import VideoStream
from pyzbar import pyzbar
import argparse
import datetime
import imutils
import time
import cv2 as cv
import winsound


frequency = 2500
duration = 1000

ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", type=str, default="barcodes_camera.csv",
                help="Path to output csv file")
args = vars(ap.parse_args())

print("[MESSAGE] [Opening webcam]")

vs = VideoStream(src=0).start()
time.sleep(2.0)

csv = open(args["output"], "w")
found = set()

while True:
    frame = vs.read()
    frame = imutils.resize(frame, width=600)

    barcodes = pyzbar.decode(frame)  # decode

    for barcode in barcodes:
        (x, y, w, h) = barcode.rect
        cv.rectangle(frame, (x, y), (x + w, y + h), (0, 155, 255), 2)
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type

        text = "{} ({})".format(barcodeData, barcodeType)
        cv.putText(frame, text, (x, y - 10),
                    cv.FONT_HERSHEY_SIMPLEX, 0.5, (155, 0, 255), 2)

        if barcodeData not in found:
            csv.write("{},{}\n".format(datetime.datetime.now(),
                                       barcodeData))
            csv.flush()
            found.add(barcodeData)
            winsound.Beep(frequency, duration)

    cv.imshow("Barcode Scanner", frame)
    key = cv.waitKey(1) & 0xFF

    if key == ord("q"):
        break

print("[MESSAGE] [Cleaning up the file]")
csv.close()

cv.destroyAllWindows()

vs.stop()
