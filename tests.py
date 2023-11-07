import os
from dec import logger_func, logger
from old import get_article_date, get_article_header, get_actual_link, make_soup, check_article_body, \
    _get_response
KEYWORDS = ['дизайн', 'фото', 'web', 'python', 'Wasteland', 'ViRush', 'нейросеть', 'робот']

def test_1():
    path = 'main.log'
    if os.path.exists(path):
        os.remove(path)

    @logger
    def hello_world():
        return 'Hello World'

    @logger
    def summator(a, b=0):
        return a + b

    @logger
    def div(a, b):
        return a / b

    assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
    result = summator(a=2, b=2)
    assert isinstance(result, int), 'Должно вернуться целое число'
    assert result == 4, '2 + 2 = 4'
    result = div(a=6, b=2)
    assert result == 3, '6 / 2 = 3'

    assert os.path.exists(path), 'файл main.log должен существовать'

    summator(a=4.3, b=2.2)
    summator(a=0, b=0)

    with open(path) as log_file:
        log_file_content = log_file.read()

    assert 'summator' in log_file_content, 'должно записаться имя функции'
    for item in (4.3, 2.2, 6.5):
        assert str(item) in log_file_content, f'{item} должен быть записан в файл'


def test_2():
    paths = ('log_1.log', 'log_2.log', 'log_3.log')

    for path in paths:
        if os.path.exists(path):
            os.remove(path)

        @logger_func(path)
        def hello_world():
            return 'Hello World'

        @logger_func(path)
        def summator(a, b=0):
            return a + b

        @logger_func(path)
        def div(a, b):
            return a / b

        assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
        result = summator(2, 2)
        assert isinstance(result, int), 'Должно вернуться целое число'
        assert result == 4, '2 + 2 = 4'
        result = div(6, 2)
        assert result == 3, '6 / 2 = 3'
        summator(4.3, b=2.2)

    for path in paths:

        assert os.path.exists(path), f'файл {path} должен существовать'

        with open(path) as log_file:
            log_file_content = log_file.read()

        assert 'summator' in log_file_content, 'должно записаться имя функции'

        for item in (4.3, 2.2, 6.5):
            assert str(item) in log_file_content, f'{item} должен быть записан в файл'


def test_3():  # тест по старой ДЗ
    url = 'https://habr.com/ru'  # базовый url
    response = _get_response(some_url=url)  # переменная сделана для проверки работы логгера.
    soup = make_soup(some_url=url)  # делаем из полученной строки суп

    articles = soup.findAll('article')  # ищем все заданные тэги
    for article in articles:  # обрабатываем каждый тэг
        full_article_url = get_actual_link(article=article)  # ссылка на полную статью
        article_soup = make_soup(full_article_url)  # получаем суп из полной статьи.
        article_word_set = check_article_body(full_article_soup=article_soup)  # множество из слов из тела статьи

        for word in KEYWORDS:  # проверка вхождения требуемых слов в тело полной статьи
            if word.lower() in article_word_set:
                article_date = get_article_date(article=article_soup)
                header = get_article_header(article=article_soup)
                print(f'Дата: {article_date}. Название статьи - {header}, '
                      f'ссылка - {full_article_url}')