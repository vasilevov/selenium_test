import config
from selenium.webdriver.common.by import By

driver = config.driver

#Проверка соответствия URL
def test_url_check_OK():
    driver.get('https://qa-mesto.praktikum-services.ru/')
    assert '/signin' in driver.current_url
    driver.quit()

#Тест. Количество изображений больше 1
def test_find_more_than_one_images_OK():
    driver.get('https://qa-mesto.praktikum-services.ru/')
    images = driver.find_elements(By.XPATH, ".//img")
    assert len(images) > 1
    driver.quit()

#Проверка соответсвия текста плейсхолдера
def test_check_placeholder_for_email_and_password_OK():
    driver.get('https://qa-mesto.praktikum-services.ru/')
    email_field = driver.find_element(By.ID, "email")
    password_field = driver.find_element(By.ID, "password")
    assert email_field.get_attribute('placeholder') == 'Email'
    assert password_field.get_attribute('placeholder') == 'Пароль'
    driver.quit()

#Логин с корректными параметрами
def test_login_with_correct_parameters_OK():
    config.login()
    assert driver.current_url == 'https://qa-mesto.praktikum-services.ru/'
    driver.quit()

#Проверка текста на кнопке выхода из профиля
def test_check_logout_button_text_OK():
    config.login()
    assert driver.find_element(By.CLASS_NAME, "header__logout").text == 'Выйти'
    driver.quit()

#Проверка смены изображения в профиле на новое и обратно
def test_change_profile_picture_OK():
    config.login()
    old_avatar_url = driver.find_element(By.CLASS_NAME, 'profile__image').value_of_css_property("background-image").split('"')[1]
    new_avatar_url = 'https://code.s3.yandex.net/qa-automation-engineer/python/files/avatarSelenium.png'
    driver.find_element(By.CLASS_NAME, 'profile__image').click()
    driver.find_element(By.ID, 'owner-avatar').send_keys(new_avatar_url)
    driver.find_element(By.XPATH, ".//form[@name='edit-avatar']/button[text()='Сохранить']").click()
    driver.refresh()
    config.wait(30)
    assert new_avatar_url in driver.find_element(By.CLASS_NAME, 'profile__image').get_attribute('style')

    driver.find_element(By.CLASS_NAME, 'profile__image').click()
    driver.find_element(By.ID, 'owner-avatar').send_keys(old_avatar_url)
    driver.find_element(By.XPATH, ".//form[@name='edit-avatar']/button[text()='Сохранить']").click()
    driver.refresh()
    config.wait(30)
    assert old_avatar_url in driver.find_element(By.CLASS_NAME, 'profile__image').get_attribute('style')

    driver.quit()

#Добавление новой карточки, проверка названия карточки, удаление
def test_add_new_card_check_name_delete_card_OK():
    config.login()
    title_before = config.get_last_card().find_element(By.CLASS_NAME, 'card__title').text
    new_title = config.get_cardname_with_time()
    image_link = 'https://code.s3.yandex.net/qa-automation-engineer/python/files/photoSelenium.jpeg'
    driver.find_element(By.CLASS_NAME, 'profile__add-button').click()
    driver.find_element(By.ID, 'place-name').send_keys(new_title)
    driver.find_element(By.ID, 'place-link').send_keys(image_link)
    driver.find_element(By.XPATH, ".//form[@name='new-card']/button[text()='Сохранить']").click()
    driver.refresh()
    config.wait(30)
    assert config.get_last_card().find_element(By.CLASS_NAME, 'card__title').text == new_title

    card_count_before = driver.find_elements(By.XPATH, ".//li[@class='places__item card']").__len__()
    config.get_last_card().find_element(By.CLASS_NAME, 'card__delete-button').click()
    driver.refresh()
    config.wait(30)
    card_count_after = driver.find_elements(By.XPATH, ".//li[@class='places__item card']").__len__()
    assert card_count_before == card_count_after + 1

    driver.quit()
