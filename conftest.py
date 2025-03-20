import pytest
import os

SCREENSHOTS_DIR = "tools/allure_2_32/screenshots"
ALLURE_RESULTS = "reports/allure-results"


@pytest.fixture(scope="session", autouse=True)
def clean_screenshot_folder():
    if os.path.exists(SCREENSHOTS_DIR):
        for file_name in os.listdir(SCREENSHOTS_DIR):
            file_path = os.path.join(SCREENSHOTS_DIR, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)

    yield


@pytest.fixture(scope="session", autouse=True)
def clean_allure_results_folder():
    if os.path.exists(ALLURE_RESULTS):
        for file_name in os.listdir(ALLURE_RESULTS):
            file_path = os.path.join(ALLURE_RESULTS, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)

    yield

