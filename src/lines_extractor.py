import pdfplumber


class LinesExtractor:

    def get_all_lines(self, file):
        with pdfplumber.open(file) as pdf:
            return pdf.pages[0].extract_text().split("\n")
