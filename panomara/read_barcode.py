from pyzbar.pyzbar import decode
import cv2
filename = "/home/alberto/PycharmProjects/kinder/find barcode into images/hgchjgcsjhdcjs"
img = cv2.imread(filename)
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
barcodes = decode(gray_img)
barcode=barcodes[0].data
print(barcode)
