from src.pdf_parser import PDFParser
from tools.pdf_to_image_for_allure import pdf_to_image, attach_image
import pytest
import allure
from tools.create_test_data_and_ref import data, reference


@pytest.mark.parametrize("initial_pdf_path", reference)
@pytest.mark.parametrize("tested_pdf_path", data)
@allure.suite("Тут тест сюит для значений полей")
@allure.sub_suite("Тут саб суит для значений полей")
class TestFields:
    @allure.title("тут название теста. динамическую тест дату сюда не впихнуть")
    def test_fields(self, initial_pdf_path, tested_pdf_path):
        with allure.step(f"Поехали. Тестируем {tested_pdf_path}"):
            initial_pdf = PDFParser(initial_pdf_path)
            testing_pdf = PDFParser(tested_pdf_path)
        with allure.step(f"Сверка каждого ключа тест файла с референсом"):
            for initial_key, testing_key in zip(initial_pdf.parse().keys(), testing_pdf.parse().keys()):
                try:
                    assert testing_key == initial_key, f"Check {testing_key} and {initial_key} fields"
                except AssertionError as e:
                    with allure.step(f"Ключи не совпадают. Смотри скриншоты"):
                        initial_image = pdf_to_image(initial_pdf_path)
                        tested_image = pdf_to_image(tested_pdf_path)
                        attach_image(initial_image, tested_image)

                        raise e
