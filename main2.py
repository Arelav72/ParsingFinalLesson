import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Инициализируем браузер
driver = webdriver.Firefox()
# Если мы используем Chrome, пишем
# driver = webdriver.Chrome()

# В отдельной переменной указываем сайт, который будем просматривать
url = "https://www.mirlustr.ru/category/lyustry/"

# Функция для парсинга текущей страницы
def parse_current_page():
    lustras = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'products-thumbs__wrapper')))
    for lustra in lustras:
        try:
            # Находим элементы внутри карточек по значению
            title = lustra.find_element(By.CSS_SELECTOR, 'a.product-thumb__name').text
            price = lustra.find_element(By.CSS_SELECTOR, 'span.price').text
            link = lustra.find_element(By.CSS_SELECTOR, 'a.product-thumb__name').get_attribute('href')

            # Вносим найденную информацию в список
            parsed_data.append([title, price, link])

            # Выводим информацию о люстре в консоль для проверки
            print(f"Название: {title}, Цена: {price}, Ссылка: {link}")
        except Exception as e:
            print(f"Произошла ошибка при парсинге: {e}")
            continue

# Открываем веб-страницу
driver.get(url)

# Устанавливаем время ожидания в 20 секунд
wait = WebDriverWait(driver, 20)

parsed_data = []  # Создаём список, в который потом всё будет сохраняться

try:
    while True:
        # Парсим текущую страницу
        parse_current_page()

        try:
            # Ищем кнопку "Следующая страница" и кликаем по ней
            next_button = driver.find_element(By.CSS_SELECTOR, 'a.next.page-numbers')
            next_button.click()

            # Ждем, пока загрузится следующая страница
            wait.until(EC.staleness_of(next_button))
        except NoSuchElementException:
            # Если кнопка "Следующая страница" не найдена, значит мы на последней странице
            break
except TimeoutException:
    print("TimeoutException: Элементы не найдены в течение заданного времени")
finally:
    # Закрываем подключение браузера
    driver.quit()

# Проверяем, есть ли данные для записи
if parsed_data:
    # Прописываем открытие нового файла, задаём ему название и форматирование
    with open("lustras.csv", 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Название', 'Цена', 'Ссылка'])
        writer.writerows(parsed_data)
    print("Данные успешно сохранены в lustras.csv")
else:
    print("Нет данных для записи")