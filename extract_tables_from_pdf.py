import camelot
import pandas as pd


def extract_and_combine_tables_from_pdf(pdf_file: str) -> pd.DataFrame:
    """
    Извлекает таблицы из PDF файла и объединяет их в один DataFrame.

    :param pdf_file: Путь к PDF файлу.
    :return: Объединенный DataFrame, содержащий данные из всех таблиц.
    """
    all_data = []

    try:
        tables = camelot.read_pdf(pdf_file,
                                  strip_text='\n',
                                  line_scale=40,
                                  split_text=True,
                                  pages='all')
        for table in tables:
            all_data.append(table.df)

        # Объединяем все таблицы в один DataFrame
        whole_table = pd.concat(all_data, ignore_index=True)

    except Exception as e:
        print(f"Произошла ошибка при обработке файла {pdf_file}: {e}")
        return pd.DataFrame()  # Возвращаем пустой DataFrame в случае ошибки

    return whole_table
