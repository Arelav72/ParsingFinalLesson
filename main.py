# Импортируем модуль со временем
import time
# Импортируем модуль csv
import csv
# Импортируем Selenium
from selenium import webdriver
from selenium.webdriver.common.by import By

# Инициализируем браузер
driver = webdriver.Firefox()
# Если мы используем Chrome, пишем
# driver = webdriver.Chrome()

# В отдельной переменной указываем сайт, который будем просматривать
url = "https://www.mirlustr.ru/category/lyustry/"

# Открываем веб-страницу
driver.get(url)

# Задаём 5 секунд ожидания, чтобы веб-страница успела прогрузиться
time.sleep(5)
# Находим все карточки с вакансиями с помощью названия класса
# Названия классов берём с кода сайта
lusrtas = driver.find_elements(By.CLASS_NAME, 'products-thumbs__wrapper')

# Выводим количество найденных вакансий
print(f"Найдено вакансий: {len(lusrtas)}")
# Создаём список, в который потом всё будет сохраняться
parsed_data = []
# Создаём список, в который потом всё будет сохраняться
parsed_data = []

# Перебираем коллекцию люстр
# Используем конструкцию try-except, чтобы "ловить" ошибки, как только они появляются
for lusrta in lusrtas:
    try:
        # Находим элементы внутри карточек по значению
        # Находим название люстры
        title = lusrta.find_element(By.CSS_SELECTOR, 'a.product-thumb__name').text
        # Находим цену
        price = lusrta.find_element(By.CSS_SELECTOR, 'span.price').text

        # Находим ссылку с помощью атрибута 'href'
        link = lusrta.find_element(By.CSS_SELECTOR, 'a.product-thumb__name').get_attribute('href')

        # Вносим найденную информацию в список
        parsed_data.append([title, price, link])

        # Выводим информацию о люстре в консоль для проверки
        print(f"Название: {title}, Цена: {price}, Ссылка: {link}")
    except Exception as e:
        print(f"Произошла ошибка при парсинге: {e}")
        continue

# Закрываем подключение браузера
driver.quit()

# Проверяем, есть ли данные для записи
if parsed_data:
    # Прописываем открытие нового файла, задаём ему название и форматирование
    # 'w' означает режим доступа, мы разрешаем вносить данные в таблицу
    with open("lustras.csv", 'w', newline='', encoding='utf-8') as file:
        # Прописываем форматирование
        writer = csv.writer(file)
        # Создаём первый ряд
        writer.writerow(['Название', 'Цена', 'Ссылка'])

        # Прописываем использование списка как источника для рядов таблицы
        writer.writerows(parsed_data)
    print("Данные успешно сохранены в lustras.csv")
else:
    print("Нет данных для записи")