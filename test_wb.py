import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture()
def browser():
   browser=webdriver.Chrome()
   yield browser
   browser.quit()
def test_for_wb(browser):
    open_link=browser.get("https://www.wildberries.ru/")
    #Ищем лого
    logo=browser.find_element(By.CLASS_NAME,'nav-element__logo') 
    assert logo.is_displayed(), "Логотип не найден"
    #Ищем кнопку поиска
    search = browser.find_element(By.ID, 'searchInput')
    #Вбиваем в поиск "Сумка"
    search.send_keys('Сумка')
    search.send_keys(Keys.RETURN)
    #Ожидание отклика и поиск товара
    WebDriverWait(browser, 40).until(
        EC.presence_of_element_located((By.CLASS_NAME, "j-open-full-product-card"))
    )
    card_first=browser.find_element(By.CLASS_NAME,'j-open-full-product-card')
    #Скроллим до товара
    browser.execute_script("arguments[0].scrollIntoView();", card_first)

    if not card_first:
        assert False, "Товары не найдены"
    #Обращаемся к названию товара, буквы переводим в строчный вид
    product_name = card_first.get_attribute("aria-label").lower()
    #Проверяем наличие подстроки "сумка"
    assert "сумка" in product_name, "Найденный товар не является сумкой"
    #Ждем и добавляем товар в корзину
    add_card = WebDriverWait(browser, 40).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'btn-icon__white'))
    )
    add_card.click()
    #Открываем корзину после ожидания
    shopping_bag=WebDriverWait(browser, 40).until(
        EC.presence_of_element_located((By.CLASS_NAME,"navbar-pc__icon--basket"))
    )
    shopping_bag.click()
    # Проверка наличия добавленного товара в корзине
    WebDriverWait(browser, 40).until(
        EC.presence_of_element_located((By.CLASS_NAME, "good-info__good-name"))
    )

    # Проверка наличия добавленного товара в корзине
    cart_items = browser.find_elements(By.CLASS_NAME, "good-info__good-name")
    found = False
    for item in cart_items:
        # Прокрутка страницы до элемента
        browser.execute_script("arguments[0].scrollIntoView();", item)
        item_title = item.text.lower()
        if "сумка" in item_title:
            found = True
            break

    assert found, "Товар не найден в корзине"
# Вывод сообщения о добавлении товара в корзину
    print("Товар добавлен в корзину")

    # Вывод сообщения об успешном прохождении теста
    print("Тест прошел успешно")

# Запуск теста
if __name__ == "__main__":
    pytest.main()    