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


def login(driver):
    # user_name = input('Phone number, username or email: ')
    # password = pyip.inputPassword('password: ')

    try:
        log_in = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, '_aa48')))
        print('Element found!')
        log_in.send_keys('zzhopewhite@gmail.com', Keys.TAB, 'Zumfara!1', Keys.ENTER)
        print('Entering pass and user')
    except:
        print('There was a problem with log in !')
        print('Try again!')

def next_page_check(driver, url):
    counter = 0
    while counter != 5:
        if driver.current_url != url:
            print('Sucses!')
            break
        else:
            time.sleep(1)
            counter += 1


def main():
    url = 'https://www.instagram.com/'
    driver = initialize_driver()
    driver.get(url)
    login(driver)
    create_folder()
    download_img()
    

def create_folder():
    os.makedirs('insta_img', exist_ok=True)


def download_img():

    request = requests.get('https://www.instagram.com/gugizm/')
    try:
        request.raise_for_status()
        print('Everything ok!!!')
    except:
        print("there was a problem")
    
    soap = bs4.BeautifulSoup(request.text, 'lxml')
    img_list = soap.select('.x1iyjqo2 img')
    print(img_list)
    for img in img_list:
        url = img.get('src')
        print(url)
        res = requests.get(url)
        try:
            res.raise_for_status()
            print(f'downloading img {url}')
        except:
            print('Could not found img')
        with open(os.path.join('insta_img', os.path.basename(url)), 'wb') as file:
            for chunk in res.iter_content(100000):
                file.write(chunk)

main()

#x1iyjqo2
#cklikibng search
    #need requests download page 
#typing user
#downloading content
