import glob
from PyPDF2 import PdfMerger, PdfReader
from datetime import datetime
import os

SEARCH_KEY = 'Страни*.pdf'


def merge_pdfs(folder_path: str) -> str:
    """
    Объединяет все PDF-файлы в один PDF-файл с текущей датой в названии.

    :param folder_path: Путь к папке, содержащей PDF-файлы.
    :return: Путь к объединенному PDF-файлу.
    """
    merger = PdfMerger()

    pdf_files = glob.glob(os.path.join(folder_path, SEARCH_KEY))

    if not pdf_files:
        raise FileNotFoundError(
            f'Файлы по ключу: {SEARCH_KEY} в папке: {folder_path} не найдены!'
        )

    for file_path in pdf_files:
        merger.append(file_path)

    current_date = datetime.now().strftime("%Y-%m-%d")
    output_pdf = f'объединенный_файл_{current_date}.pdf'

    merger.write(output_pdf)
    merger.close()

    return output_pdf


def get_number_of_pages(pdf_file: str) -> int:
    """
    Получает количество страниц в PDF-файле.

    :param pdf_file: Путь к PDF-файлу.
    :return: Количество страниц.
    """
    with open(pdf_file, "rb") as file:
        reader = PdfReader(file)
        num_pages = len(reader.pages)
    return num_pages
