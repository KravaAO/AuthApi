def mock_classify_columns(df):
    possible_names = ['Назва', 'Кількість', 'Міста', 'Рейтинг', 'Категорія', 'Дата', 'Сфера', 'Тип']
    return [possible_names[i % len(possible_names)] for i in range(len(df.columns))]
