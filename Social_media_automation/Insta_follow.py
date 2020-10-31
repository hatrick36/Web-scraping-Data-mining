# The following program uses selenium to navigate and interact with he instagram platform to follow profiles on the
# the users suggested page
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import os
import time


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
        self.driver = webdriver.Chrome('chromedriver80.exe')
        self.base_url = 'https://www.instagram.com'
        self.login()

    def login(self):
        # calls chromedriver defined in __init__ navigate to the base url with the formatted text
        self.driver.get('{}/accounts/login/'.format(self.base_url))
        # utilizes webDriverWait to allow chromedriver to load page then clicks and enters credentials via 'send_keys'
        username_element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))
        username_element.send_keys(self.username)
        self.driver.find_element_by_name('password').send_keys(self.password)
        #sleep is thorn in to allow pages to load
        time.sleep(1)
        self.driver.find_elements_by_xpath("//div[contains(text(), 'Log In')]")[0].click()
        time.sleep(3)
    def nav_page(self, page):
        # navigates to page specified with kwarg 'page' called in main
        self.driver.get('{}/{}/'.format(self.base_url, page))

    def follow_user(self):
        #I put a timer on this function to run for and hour
        timer = time.time()
        period = 60*60
        # finds allow 'follow buttons on the explore page and puts them in a list
        follow_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//button[ "
                                                           "contains("
                                                           "text(), "
                                                           "'Follow')]")))
        print(len(follow_button))
        print(timer)
        #the for loop iterates through the list of follow buttons clicking every 30 seconds because instagram limits follows by time
        for follow_button in follow_button:

            follow_button.click()
            time.sleep(30)
            if time.time() > timer + period:
                break


if __name__ == '__main__':
    ig_bot = Instabot('USERNAME', 'PASSWORD')
    time.sleep(3)
    ig_bot.nav_page('explore/people/suggested')
    ig_bot.follow_user()

    print(Instabot.username)
