from src.lines_extractor import LinesExtractor
from src.key_value_converter import KeyValueConverter
from src.barcode_reader import BarcodeReader


class PDFParser:
    def __init__(self, path_to_file):
        self.__file = path_to_file
        self.__parsed_info = {}
        self.__extractor = LinesExtractor()
        self.__converter = KeyValueConverter()
        self.__barcode_reader = BarcodeReader()

    def parse(self):
        all_lines = self.__extractor.get_all_lines(self.__file)
        for line in all_lines:
            if ":" not in line:
                if "TITLE" not in self.__parsed_info:
                    self.__parsed_info["TITLE"] = line
                else:
                    self.__parsed_info["NOTES"] = line
            else:
                has_two_colons = ":" in line and line.count(":") == 2
                self.__parsed_info.update(self.__converter.convert_keys_values_to_dict(has_two_colons, line))
        self.__parsed_info.update(self.__barcode_reader.add_barcodes(self.__file))
        return self.__parsed_info

    def get_barcodes(self):
        return self.__barcode_reader.get_barcodes()

