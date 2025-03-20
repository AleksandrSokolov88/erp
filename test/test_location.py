from src.pdf_parser import PDFParser
import pdfplumber
import pytest
import allure
from tools.create_test_data_and_ref import data, reference
from tools.pdf_to_image_for_allure import pdf_to_image, attach_image
from tools.coordinate_rounding import round_


@pytest.mark.parametrize("initial_pdf_path", reference)
@pytest.mark.parametrize("tested_pdf_path", data)
@allure.suite("Тут тест сюит для координат")
@allure.sub_suite("Тут саб суит для координат")
class TestLocation:
    @allure.title("тут название теста. динамическую тест дату сюда не впихнуть")
    def test_location(self, initial_pdf_path, tested_pdf_path):
        with (allure.step(f"Поехали. тестируем {tested_pdf_path}")):
            initial_pdf = PDFParser(initial_pdf_path)
            testing_pdf = PDFParser(tested_pdf_path)

            with pdfplumber.open(initial_pdf_path) as pdf:
                all_words_initial = pdf.pages[0].extract_words()

            with pdfplumber.open(tested_pdf_path) as pdf:
                all_words_testing = pdf.pages[0].extract_words()

            list_keys_initial = list(initial_pdf.parse().keys())
            for i in list_keys_initial:
                if " " in i:
                    list_keys_initial.extend(i.split())
                    list_keys_initial.remove(i)

            list_keys_testing = list(testing_pdf.parse().keys())
            for i in list_keys_testing:
                if " " in i:
                    list_keys_testing.extend(i.split())
                    list_keys_testing.remove(i)

        with allure.step("Вычисляем координаты для всех элементов"):
            try:
                initial_dict = {}
                for i in all_words_initial:
                    if i["text"] in initial_pdf.parse()["TITLE"] or i["text"].replace(":", "") in list_keys_initial:
                        initial_dict[i["text"].replace(":", "")] = {"x0": round_(i["x0"]), "x1": round_(i["x1"]),
                                                                    "top": round_(i["top"]),
                                                                    "bottom": round_(i["bottom"])}

                initial_dict["main_barcode"] = {"left": initial_pdf.get_barcodes()[0]["location"][0],
                                                "top": initial_pdf.get_barcodes()[0]["location"][1],
                                                "width": initial_pdf.get_barcodes()[0]["location"][2],
                                                "height": initial_pdf.get_barcodes()[0]["location"][3]}
                initial_dict["changible_barcode"] = {"left": initial_pdf.get_barcodes()[1]["location"][0],
                                                     "top": initial_pdf.get_barcodes()[1]["location"][1],
                                                     "width": initial_pdf.get_barcodes()[1]["location"][2],
                                                     "height": initial_pdf.get_barcodes()[1]["location"][3]}

                testing_dict = {}
                for i in all_words_testing:
                    if i["text"] in testing_pdf.parse()["TITLE"] or i["text"].replace(":", "") in list_keys_testing:
                        testing_dict[i["text"].replace(":", "")] = {"x0": round_(i["x0"]),
                                                                    "x1": round_(i["x1"]),
                                                                    "top": round_(i["top"]),
                                                                    "bottom": round_(i["bottom"])}

                testing_dict["main_barcode"] = {"left": testing_pdf.get_barcodes()[0]["location"][0],
                                                "top": testing_pdf.get_barcodes()[0]["location"][1],
                                                "width": testing_pdf.get_barcodes()[0]["location"][2],
                                                "height": testing_pdf.get_barcodes()[0]["location"][3]}
                testing_dict["changible_barcode"] = {"left": testing_pdf.get_barcodes()[1]["location"][0],
                                                     "top": testing_pdf.get_barcodes()[1]["location"][1],
                                                     "width": testing_pdf.get_barcodes()[1]["location"][2],
                                                     "height": testing_pdf.get_barcodes()[1]["location"][3]}

            except Exception as e:
                with allure.step(
                        "Проблема с элементами. До координат не добрались. Запусти эту тест дату на test_fields"):
                    initial_image = pdf_to_image(initial_pdf_path)
                    tested_image = pdf_to_image(tested_pdf_path)
                    attach_image(initial_image, tested_image)

                    raise e

        with allure.step("Сверяем координаты"):
            for i in initial_dict:
                try:

                    assert initial_dict[i] == testing_dict[i], (f" \n {i} "
                                                                f"diff {initial_dict[i]} and {testing_dict[i]}")
                except AssertionError as e:
                    diff = {}
                    for key_initial in initial_dict[i]:

                        if initial_dict[i][key_initial] - testing_dict[i][key_initial] != 0:
                            diff[key_initial] = initial_dict[i][key_initial] - testing_dict[i][key_initial]
                    with allure.step(
                            f"Координаты не совпадают для поля {i} с разницей {diff} от референса . Смотри скриншоты"):
                        initial_image = pdf_to_image(initial_pdf_path)
                        tested_image = pdf_to_image(tested_pdf_path)
                        attach_image(initial_image, tested_image)
                    raise e
                except KeyError as e:
                    with allure.step("Что то не так с ключами"):
                        initial_image = pdf_to_image(initial_pdf_path)
                        tested_image = pdf_to_image(tested_pdf_path)
                        attach_image(initial_image, tested_image)
                        raise e
