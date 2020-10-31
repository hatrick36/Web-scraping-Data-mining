from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import os
import pandas as pd
import time
from selenium.common.exceptions import NoSuchElementException


# IMPORTANT: don't try to grab multiple lists from this script just get likers and followers import any other lists

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

    def get_likes(self, amount):

        global likes
        time.sleep(1)
        self.driver.find_element_by_class_name('_bz0w').click()
        i = 1
        while i <= amount:
            time.sleep(2)
            try:
                self.driver.find_element_by_xpath(
                    '/html/body/div[4]/div[2]/div/article/div[2]/section[2]/div/div[2]/button').click()
                likes = self.get_names()
                print(likes)
            except NoSuchElementException:
                print('not enough activity on post')
                self.driver.find_element_by_xpath(
                    '/html/body/div[4]/div[2]/div/article/div[2]/section[2]/div/div[1]').click()
                continue
            i += 1
        df = pd.DataFrame.from_dict({'likes': likes}, orient='index').T

        df.to_csv('follow.csv')
        print(df)

    def get_names(self):
        time.sleep(1)
        scroll_box = self.driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div')
        last_ht, ht = 0, 1
        while last_ht != ht:
            last_ht = ht
            time.sleep(1)
            ht = self.driver.execute_script("""
                    arguments[0].scrollTo(0, arguments[0].scrollHeight)
                    return arguments[0].scrollHeight""", scroll_box)
        links = scroll_box.find_elements_by_tag_name('a')
        names = [name.text for name in links if name.text != '']
        self.driver.find_elements_by_xpath('/html/body/div[5]/div/div[1]/div/div[2]/button')[0].click()
        self.driver.find_element_by_class_name('_65Bje').click()
        return names


if __name__ == '__main__':
    ig_bot = Instabot('_patrick_dowd_', 'Crabapple10')
    time.sleep(3)
    ig_bot.nav_page('_patrick_dowd_')
    ig_bot.get_likes(5)
    ig_bot.get_names()
    print(Instabot.username)
