import pandas as pd


def process_table(raw_table: pd.DataFrame) -> pd.DataFrame:
    """
    Обрабатывает таблицу, извлекая заголовок, удаляя ненужные строки,
    объединяя строки и очищая данные.

    :param whole_table: Исходный DataFrame.
    :return: Обработанный DataFrame.
    """
    # Извлекаем заголовок из первой строки
    header = raw_table.iloc[0]

    # Удаляем строки, которые содержат значения заголовка
    raw_table = raw_table[
        ~raw_table.apply(lambda row: row.isin(header).any(), axis=1)
    ]

    # Устанавливаем заголовок DataFrame
    raw_table.columns = header

    # Заменяем пустые строки на None
    raw_table = raw_table.where(raw_table != '', None)

    def combine_rows(row, prev_row):
        """
        Объединение текущей строки с предыдущей, если '№ п/п' is None.

        :param row: Текущая строка
        :param prev_row: Предыдущая строка
        :return: Объединенная строка
        """
        if row['№ п/п'] is None and row.notna().any():
            for col in row.index:
                if pd.notna(row[col]):
                    prev_row[col] = f"{prev_row[col]} {row[col]}"
        return prev_row

    # Создаем копию raw_table для изменения
    copy_raw_table = raw_table.copy()

    # Объединяем строки
    for i in range(1, len(copy_raw_table)):
        copy_raw_table.iloc[i-1] = combine_rows(
            copy_raw_table.iloc[i], copy_raw_table.iloc[i-1]
        )

    result_table = copy_raw_table

    # Удаляем строки с None в столбце '№ п/п'
    result_table = result_table[result_table['№ п/п'].notna()]

    return result_table
