from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
import time

def search_wikipedia(query):
    # Укажите путь к вашему драйверу, если он не находится в PATH
    driver = webdriver.Chrome()

    try:
        # Откройте Википедию
        driver.get("https://www.wikipedia.org/")

        # Найдите поле ввода для поиска
        search_box = driver.find_element(By.NAME, "search")

        # Введите запрос и нажмите Enter
        search_box.send_keys(query + Keys.RETURN)

        # Подождите, пока загрузится страница
        time.sleep(2)

        while True:
            paragraphs = driver.find_elements(By.CSS_SELECTOR, "p")

            action = input("\nВыберите действие:\n1. Листать параграфы\n2. Перейти на связанную страницу\n3. Выйти\n")

            if action == '1':
                browse_paragraphs(paragraphs)
            elif action == '2':
                related_page = choose_related_page(driver)
                if related_page:
                    driver.get(related_page.get_attribute('href'))
            elif action == '3':
                break
            else:
                print("Неверный ввод. Пожалуйста, выберите 1, 2 или 3.")

    finally:
        # Закройте браузер
        driver.quit()

def browse_paragraphs(paragraphs):
    index = 0
    while index < len(paragraphs):
        print(paragraphs[index].text)
        next_action = input("\nВведите 'n' для следующего параграфа или 'q' для выхода: ")
        if next_action == 'n':
            index += 1
        elif next_action == 'q':
            break
        else:
            print("Неверный ввод. Пожалуйста, введите 'n' или 'q'.")

def choose_related_page(driver):
    links = driver.find_elements(By.CSS_SELECTOR, "#bodyContent a")
    print("\nСвязанные страницы:")
    for i, link in enumerate(links[:10]):
        print(f"{i + 1}. {link.get_attribute('title') or link.text}")

    choice = input("\nВведите номер, чтобы перейти на соответствующую страницу, или 'q' для отмены: ")
    if choice.isdigit() and 1 <= int(choice) <= len(links[:10]):
        return links[int(choice) - 1]
    elif choice == 'q':
        return None
    else:
        print("Неверный выбор.")
        return None

def main():
    query = input("Введите поисковый запрос на Википедии: ")
    search_wikipedia(query)

if __name__ == "__main__":
    main()