from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import os
import time
import pandas as pd


class Instabot(object):
    username = None
    """
    initializes an instance of the Instabot class.
        
    Call the login function to authenticate a user with IG
    
    Args:
        username:str: The instagram username for the user
        password:str: The instagram password for the user
        
    Attributes:
            driver.Selenium.webdriver.Chrome: The chromedriver that is used to automate browser activity
    """

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = webdriver.Chrome('../chromedriver80.exe')
        self.base_url = 'https://www.instagram.com'
        self.login()

    def login(self):
        self.driver.get('{}/accounts/login/'.format(self.base_url))
        username_element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))
        username_element.send_keys(self.username)
        self.driver.find_element_by_name('password').send_keys(self.password)
        time.sleep(1)
        self.driver.find_elements_by_xpath("//div[contains(text(), 'Log In')]")[0].click()

    def nav_page(self, page):
        self.driver.get('{}/{}/'.format(self.base_url, page))
        time.sleep(2)

    def get_following_data(self):
        timer = time.perf_counter()
        self.driver.find_element_by_xpath('//a[contains(@href, "/following")]').click()
        following = self.get_names()
        time.sleep(1)
        following_data = [user for user in following]
        n = []
        print(following_data)
        print(len(following_data))
        print(timer)
        df = pd.DataFrame.from_dict({'following': following_data, 'n': n},
                                    orient='index').T
        df.to_csv('follow.csv')
        print(df)

    def get_names(self):
        time.sleep(1)
        scroll_box = self.driver.find_element_by_class_name('isgrP')
        last_ht, ht = 0, 1
        while last_ht != ht:
            last_ht = ht
            time.sleep(1)
            ht = self.driver.execute_script("""
            arguments[0].scrollTo(0, arguments[0].scrollHeight)
            return arguments[0].scrollHeight""", scroll_box)
        links = scroll_box.find_elements_by_tag_name('a')
        names = [name.text for name in links if name.text != '']
        self.driver.find_elements_by_xpath('/html/body/div[4]/div/div[1]/div/div[2]')[0].click()
        return names


if __name__ == '__main__':
    ig_bot = Instabot('iamabot_1234', 'GAPES1029')
    time.sleep(3)
    ig_bot.nav_page('iamabot_1234')
    ig_bot.get_following_data()
    ig_bot.get_names()

    time.sleep(3)

    print(Instabot.username)
