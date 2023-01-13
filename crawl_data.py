import re
import pandas as pd
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def process_description(html):
    description = re.sub('<[^<]+?>', '', html)
    description = re.sub('&nbsp;', '', description)
    description = re.sub('&amp;', '', description)
    description = re.sub('\t', '', description)

    list_els = description.splitlines()
    list_els = list(filter(None, list_els))
    list_field = {'Hãng': 'Brand', 'Nước': 'Country',
                  'Định dạng': 'Format', 'Thể loại': 'Genre',
                  'Năm': 'Year', 'Phong cách': 'Style',
                  'Chất lượng': 'Quality'}
    dict = {}
    # Fields
    description_str = ''
    for index, string in enumerate(list_els):
        for key, value in list_field.items():
            if key in string:
                dict[value] = re.sub(f'{key}:', '', string)
    # Description Field
    start = 999
    for index, string in enumerate(list_els):
        if 'Tracklist' in string:
            start = index
        if index > start:
            description_str += string + '\n'
    dict['Description'] = description_str


    return dict


chrome_options = Options()
chrome_options.add_argument('headless')
# chrome_options.add_argument("--incognito")
chrome_options.add_argument("--window-size=1920x1080")

s = Service('msedgedriver.exe')
driver = webdriver.Edge(service=s)
wait = WebDriverWait(driver, 1)

url = "https://lpclub.vn/frontpage"
driver.get(url)

# Count number of pages
num_of_pages = driver.find_elements(By.XPATH, "//div[@class='pages']/ul/li/a")
nums = [num.get_attribute("text") for num in num_of_pages]
max_pages = int(nums[-2])

df = pd.DataFrame()
for num_page in range(1, max_pages + 1):
    nextpage_url = url + f'?page={str(num_page)}'  # https://lpclub.vn/frontpage?page=2
    driver.get(nextpage_url)
    # time.sleep(0.5)
    # Get products in homepage
    elements = driver.find_elements(By.XPATH,
                                    "//div[@class='thumb-wrapper']/a")  # <div class="thumb-wrapper"><a href="/ngot-gieo-cd"><img src="//bizweb.dktcdn.net00" class="img-fix" alt="Gieo"></a></div>

    products_url = [el.get_attribute("href") for el in elements]

    # Every product
    for product_url in products_url:
        driver.get(product_url)
        # get data in product {name:Gieo; format:CD,DVD; country:VN; brand:LPClub; year:2020; Genre:Indie,Rock; Style: Funk Indie; Quality:New,Old}
        # Thunbnail Image
        thunbnail_Image = []
        try:
            links = wait.until(EC.presence_of_all_elements_located((By.XPATH, './/div[@class="large-image clearfix"]/a')))
            for link in links:
                thunbnail_Image += [link.get_attribute('href')]
        except TimeoutException:
            pass
        thunbnail_Image = ''.join(map(str, thunbnail_Image))

        list_images = []
        # List image in galery
        try:
            # links_img = wait.until(EC.presence_of_all_elements_located((By.XPATH, './/div[@class="previews-list slides clearfix"]/div/div/div/div/a')))
            links_img = driver.find_elements(By.XPATH,
                                             './/div[@class="previews-list slides clearfix"]/div/div/div/div/a')
            for link in links_img:
                list_images += [link.get_attribute('href')]
        except TimeoutException:
            pass

        # Name
        links_name = wait.until(EC.presence_of_all_elements_located((By.XPATH, ".//div[@class='product-name']/h1")))
        for link in links_name:
            name = link.get_attribute("innerHTML")

        # Price
        links_price = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//strong[@class='sale-price']")))
        for link in links_price:
            price = link.get_attribute("innerHTML")

        # Description
        link_description = wait.until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@id='product_tabs_description']/div")))
        for link in link_description:
            description = link.get_attribute("outerHTML")
            dict_field = process_description(description)

        dict_field['Name'] = name
        dict_field['Price'] = price
        dict_field['Thunbnail'] = thunbnail_Image
        dict_field['Category'] = list_images

        # print(dict_field) #Name, Price, Thunbnail, Category, Brand, Country, Format, Genre, Year, Style, Quality, Description
        df_dictionary = pd.DataFrame([dict_field])
        df = pd.concat([df, df_dictionary], ignore_index=True)
        # print(df)

df.to_csv('product.csv', sep='\t', encoding='utf-8')

print(df)


driver.quit()
