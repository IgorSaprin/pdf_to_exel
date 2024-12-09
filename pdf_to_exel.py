import os

from dotenv import load_dotenv
from tqdm import tqdm

from date_processing import process_table
from extract_tables_from_pdf import extract_and_combine_tables_from_pdf
from megre_pdf import get_number_of_pages, merge_pdfs

load_dotenv()
FOLDER_PATH: str = os.getenv('PDF_FOLDER_PATH')

if not FOLDER_PATH:
    raise ValueError("Ошибка: Путь к папке с PDF-файлами не задан в .env")


# Получаем объединенный pdf-файл
pdf_file: str = merge_pdfs(FOLDER_PATH)

# Получаем количкство страниц в pdf-файле
total_pages = get_number_of_pages(pdf_file)

with tqdm(total=total_pages, desc="Извлечение таблиц из PDF") as pbar:
    raw_table = extract_and_combine_tables_from_pdf(pdf_file)
    pbar.update(total_pages)

# Обрабатываем данные извлеченные из всех таблиц
result_table = process_table(raw_table)

# Сохраняем таблицу в формате .xlsx'
result_table.to_excel('ResultTable.xlsx', index=False, header=True)
