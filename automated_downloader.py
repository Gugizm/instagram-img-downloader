from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import pyinputplus as pyip
import time
import requests, bs4
import os


def initialize_driver():
    chrome_options = Options()
    chrome_options.add_experimental_option('detach', True)
    driver = webdriver.Chrome(options=chrome_options)
    return driver


def login(driver, url):
    while True:
        user_name = input('Phone number, username or email: ') #after validation error needs to clear text fildes 
        password = pyip.inputPassword('password: ')
        target_user = input('Enter target user name: ') #can taken somewhere els or change
        try:
            log_in = driver.find_element(By.CLASS_NAME, '_aa48') #change for get_element
            print('Element found!')
            log_in.send_keys(user_name, Keys.TAB, password, Keys.ENTER) # need change for inputs
            WebDriverWait(driver, 10).until(EC.url_changes(url))
            print('Login sucses!')
            return target_user
        except:
            print('There was a problem with log in !')
            print('Try again!')


def create_folder(target_user):
    os.makedirs(target_user, exist_ok=True)

def full_page_loader(driver):
    while True:
        old_source = driver.page_source
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
        time.sleep(2)
        new_source = driver.page_source
        if old_source == new_source:
            break
        old_source = new_source

def download_img(driver, user): # split this function for a parts
    cookies = driver.get_cookies()
    session = requests.Session()
    for cookie in cookies:
        session.cookies.set(cookie['name'], cookie['value'])
    
    page_source = driver.page_source
    soap = bs4.BeautifulSoup(page_source, 'lxml')
    img_list = soap.select('._aagv img')
    
    for img in img_list:
        img_url = img.get('src')
        name = str(img.get('alt')) + '.png'
        print(name)
        res = session.get(img_url)
        try:
            res.raise_for_status()
            print(f'downloading img {img_url}')
        except:
            print('Could not found img')
        with open(os.path.join(user, name), 'wb') as file:
            for chunk in res.iter_content(100000):
                file.write(chunk)


def main():
    url = 'https://www.instagram.com/'
    driver = initialize_driver()
    driver.get(url)
    user = login(driver, url)
    driver.get(url + user) #shoud take from input
    create_folder(user)
    time.sleep(5)
    full_page_loader(driver)
    download_img(driver, user)
    driver.quite()


if __name__ == "__main__":
    main()
