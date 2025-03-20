import fitz
from pyzbar.pyzbar import decode
from PIL import Image


class BarcodeReader:

    def __init__(self):
        self.__barcode_info = {}
        self.__parsed_info = {}

    def add_barcodes(self, path_to_file):
        BARCODE = "barcode"
        pdf_document = fitz.open(path_to_file)
        page = pdf_document.load_page(0)
        location = page.rect
        zoom = 3
        matrix = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=matrix, clip=location)
        image = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)

        barcode_objects = decode(image)
        for i, obj in enumerate(barcode_objects[::-1]):
            rect = obj.rect
            self.__barcode_info[i] = {BARCODE: obj.data.decode('utf-8'), "location": rect}
            self.__parsed_info["MAIN_BARCODE"] = self.__barcode_info[0][BARCODE]
        if len(self.__barcode_info) == 2:
            self.__parsed_info["TAGGED BY"] = self.__barcode_info[1][BARCODE]
        return self.__parsed_info

    def get_barcodes(self):
        return self.__barcode_info
