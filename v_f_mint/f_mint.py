import datetime
import logging
import random

import undetected_chromedriver as uc
from time import sleep

import os, sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))

from utils import telegram
from driver.base_page import BasePage

from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager

class France(BasePage):
    pass


if __name__ == "__main__":
    options = webdriver.ChromeOptions()
    options.headless = True
    # driver = uc.Chrome(options=options)
    driver = webdriver.Chrome(options=options)
    attempts = 0
    for i in range(25):
        try:
            attempts = attempts + 1
            logging.warning(f'{attempts}, {datetime.datetime.now()}')
            driver.delete_all_cookies()
            driver.get(sys.argv[1])
            f = France(driver)
            if 'Bad Gateway' not in driver.page_source:
                f.click_on('Доступ к услугам')
                if f.is_element_displayed('//button[text()="Нет"]'):
                    f.click_on('//button[text()="Нет"]')
                f.click_on('Подтвердить')
                f.click_on('Я прочитал')
                f.click_on('Назначить встречу')
                if f.is_element_displayed('//section/div'):
                    telegram.send_doc('🇫🇷 Франция появилась дата', driver.page_source)
                    f.click_on('//section/div')
                    while True:
                        if f.is_element_displayed('//p[contains(text(),"К сожалению, все наши слоты зарезервированы")]'):
                            sleep(5)
                            driver.refresh()
                            if f.is_element_displayed('//section/div'):
                                f.click_on('//section/div')
                        else:
                            telegram.send_doc('🟢 🇫🇷 Франция появился слот', driver.page_source, debug=False)
                            logging.warning('Появился Слот')
                            sleep(random.randint(100, 120))
                            driver.quit()
                            break
                elif not f.is_element_displayed('На сегодня нет свободных мест.'):
                    telegram.send_image(driver, f'Франия({attempts}): Есть даты! ')
                    telegram.send_doc(f'Франия({attempts}): Есть даты!', driver.page_source, debug=False)
                    logging.warning('Слот')
                    sleep(random.randint(100, 120))
                else:
                    sleep(random.randint(100, 120))
                logging.warning('Франция нет дат')
            else:
                # telegram.send_doc(f'Франция({attempts}): Ошибка 502', driver.page_source, debug=False)
                logging.warning(f'ООшибка 502{attempts}')
                dt = datetime.strptime(datetime.now(tz=timezone.utc).strftime('%m/%d/%Y/%H/%M/%S.%f'),
                                       '%m/%d/%Y/%H/%M/%S.%f')
                logging.warning(f'Ошибка 502{dt}')
                sleep(random.randint(50, 120))
                driver.refresh()

        except Exception as e:
            try:
                # telegram.send_doc(f'Франция({attempts}): Неизвестная ошибка', driver.page_source, debug=False)
                logging.warning(f'Ошибка 502{attempts}')
                sleep(random.randint(100, 120))
            except Exception as e:
                telegram.send_message(f'Франция({attempts}): Неизвестная ошибка\n{str(e)}', debug=False)
                sleep(random.randint(100, 120))