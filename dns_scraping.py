import os
import shutil
import time
from datetime import date, datetime
import platform
import requests
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from bs4 import BeautifulSoup
from lxml import html
import pandas as pd

start_time = datetime.now()
print(start_time)

def load_data(page):
    try:
        dns = f'https://www.dns-shop.ru/catalog/17a89aab16404e77/videokarty/?p={page}&order=1&groupBy=none&f[mv]=el42k-m2gyu-faj4z-m2gz2-k1fh8-kkiog-n20i4-kyptx-n5hup-ldmod-ddz9-h33k&stock=2' #1030 - 2080

        url = dns

        options = webdriver.ChromeOptions()
        #options.add_argument("--user-data-dir=./web_driver/selenium")
        #options.add_argument('headless')
        options.add_argument('start-maximized')
        currentpath = os.getcwd()
        pl = platform.system()
        
        chromedriver = 'chromedriver.exe' if pl == 'Windows' else 'chromedriver'
        driver = webdriver.Chrome(executable_path=f'{currentpath}/web_driver/{chromedriver}', options=options)
        print(f'Webdriver is loaded for: {pl}')

        wait = WebDriverWait(driver, 10)

        print('- Starting browser...')
        
        driver.get(url)
        print('Navigating to the website')

        # Choose city
        try:
            driver.find_element_by_xpath("//*[contains(text(), 'Самара')]")
            print('The city is already chosen')
        except (NoSuchElementException, TimeoutException):
            wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'location-icon'))).click()
            wait.until(EC.visibility_of_element_located((By.LINK_TEXT, 'Самара'))).click()
            print('The City is chosen')
        
        wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, 'select-lists state-city-select')))

        #driver.refresh()
        
        print('Waiting for price to load')
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'product-min-price__current')))
        print('Price found!')

        time.sleep(4)

        request = driver.page_source
        driver.quit()
        print('Web driver quit')
        return request
    except (NoSuchElementException, TimeoutException):
        print('No element :(')

def contain_data(text):
    try:
        soup = BeautifulSoup(text, 'lxml')
        item_list = soup.find('div', {'class': 'catalog-items-list view-simple'}) # product_category_list ; catalog-items-list view-simple (js)
        return item_list is not None
    except:
        print('Current page has no content')

def save_files():
    page = 1
    
    while True:
        data = load_data(page)
        print ('- Saving Page #%d...' % (page))

        if contain_data(data):
            with open('./_temp_pages/' + 'page_%d.html' % (page), 'w', encoding='utf-8', errors='ignore') as output_file:
                output_file.write(data)
                print('Saved!')
                page += 1
        else:
                print('No content in Page #%d > skipped' %(page))
                break

def read_file(filename):
    with open(filename, 'rb') as input_file:
        text = input_file.read()
    return text

def parse_user_datafile_bs(filename):
    results = []
    text = read_file(filename)
        
    soup = BeautifulSoup(text, 'lxml')

    #DNS
    item_list = soup.find('div', {'class': 'products-list__content'}) # product_category_list ; catalog-items-list view-simple (js)
    items = item_list.find_all('div', class_='catalog-item')

    for item in items:
        #DNS
        item_name = item.find('div', {'class': 'product-info__title-link'}).find('a').text # link_gtm-js link_pageevents-js ddl_product_link ; product-info__title-link (js)
        item_link = item.find('div', {'class': 'product-info__title-link'}).find('a').get('href')
        item_link = web_site + item_link
        item_price = str(item.find('div', {'class': 'product-min-price__current'})) # subcategory-product-item__price-num ; product-price__current (js)
        item_price = int(''.join(i for i in item_price if i.isdigit())) # re.sub("\D", "", item_price) #remove characters except digits from string
        
        results.append({
                    'item_name': item_name,
                    'item_price': item_price,
                    'item_link': item_link
                })
    return results

def temp_files_cleanup():
    print('Cleaning up the temp files from previous run')
    temp_files = os.listdir('./_temp_pages')
    for f in temp_files:
        os.remove('./_temp_pages/' + f)
    print('Clean-up done!')


web_site = 'https://www.dns-shop.ru/'
current_date = date.today()
cvs = f'{current_date}_-_dns_gpu.csv'
results = []

# MacOS hack
dir_lst = os.listdir('./_temp_pages/')
if '.DS_Store' in dir_lst:
    dir_lst.remove('.DS_Store')
    print('.DS_Store cleaned up')

#Comment if already saved
temp_files_cleanup()
save_files()


for filename in dir_lst:
    results.extend(parse_user_datafile_bs('./_temp_pages/' + filename))


df = pd.DataFrame(results)

df = df.sort_values('item_price')

df['date'] = pd.Timestamp(current_date)

df.groupby(df['item_name'])

print(df)


def export_to_cvs():  
    df.to_csv(cvs, index = False, header=True, encoding='utf-8-sig')
    print(f'Data exported to: {os.getcwd()}/{cvs}')

def copy_temp_files_to_folder():
    new_date_folder = f'1030-2070S/{current_date}'
    try:
        print(shutil.copytree('_temp_pages/', new_date_folder))
    except FileExistsError:
        print('Folder already exists! No files copied!')
    print(shutil.copy2(cvs, new_date_folder))


export_to_cvs()
copy_temp_files_to_folder()

print(f'Total time spent: {datetime.now()-start_time}')
