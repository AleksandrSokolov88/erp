import os
import fitz
import allure


def pdf_to_image(pdf_path):
    doc = fitz.open(pdf_path)
    page = doc.load_page(0)
    pix = page.get_pixmap()
    image_path = os.path.join("tools/allure_2_32/screenshots", f"{os.path.splitext(os.path.basename(pdf_path))[0]}.png")
    pix.save(image_path)
    print(os.path)
    return image_path


def attach_image(initial_image, tested_image):
    with open(initial_image, "rb") as f:
        allure.attach(f.read(), name="Initial PDF Screenshot", attachment_type=allure.attachment_type.PNG)

    with open(tested_image, "rb") as f:
        allure.attach(f.read(), name="Tested PDF Screenshot", attachment_type=allure.attachment_type.PNG)
