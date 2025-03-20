import pytest
import allure
from tools.create_test_data_and_ref import data, reference
from tools.pdf_to_image_for_allure import pdf_to_image, attach_image

from src.pdf_parser import PDFParser


@pytest.mark.parametrize("initial_pdf_path", reference)
@pytest.mark.parametrize("tested_pdf_path", data)
@allure.suite("Тут тест сюит для бар кодиков")
@allure.sub_suite("Тут саб суит для бар кодиков")
class TestBarcodes:
    @allure.title("тут название теста. динамическую тест дату сюда не впихнуть")
    def test_barcodes(self, initial_pdf_path, tested_pdf_path):
        with allure.step(f"Поехали бар кодики. Тестируем {tested_pdf_path}"):
            initial_pdf = PDFParser(initial_pdf_path)
            testing_pdf = PDFParser(tested_pdf_path)
            testing_pdf.parse()
            initial_pdf.parse()
        with allure.step("Проверяем, что бар кодика у нас 2"):
            try:
                assert len(testing_pdf.get_barcodes()) == 2
            except AssertionError as e:
                with allure.step("Бар кодиков не два"):
                    initial_image = pdf_to_image(initial_pdf_path)
                    tested_image = pdf_to_image(tested_pdf_path)
                    attach_image(initial_image, tested_image)

                    raise e
        with allure.step(
                "Проверяем, что значения баркодиков одинаковы"):
            try:
                for barcode in testing_pdf.get_barcodes():
                    assert testing_pdf.get_barcodes()[barcode]["barcode"] == initial_pdf.get_barcodes()[barcode][
                        "barcode"]
            except AssertionError as e:
                with allure.step("Значения баркодиков разные"):
                    initial_image = pdf_to_image(initial_pdf_path)
                    tested_image = pdf_to_image(tested_pdf_path)
                    attach_image(initial_image, tested_image)

                    raise e
