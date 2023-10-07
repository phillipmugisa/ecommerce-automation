from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup as Bs

BASE_URL = "http://www.jumia.ug"
options = Options()
options.headless = True

def parse_products(products_wrapper, layout=None):
    products = products_wrapper.find_all("article", attrs={"class": "prd"})
    products_data = []
    for product in products:
        image = product.select('img.img')[0]
        price = product.select('.info .prc')[0].getText()

        url = product.select("a.core")[0].get('href')
        name = product.select('.info .name')[0].getText()
        rating= product.select('.info .stars')[0].getText() if product.select('.info .stars') else None

        product_data = {
            "image": None,
            "name": name,
            "url": f"{BASE_URL}{url}",
            "price": price,
            "rating": rating
        }
        products_data.append(product_data)
    return products_data
    

def get_result_list(page_source):
    soup = Bs(page_source, "html.parser")
    products_wrapper = soup.find("div", attrs={"class": "_4cl-3cm-shs"})
    return parse_products(products_wrapper)

def product_search(product_name):
    driver = webdriver.Chrome(options=options)
    driver.get(BASE_URL)
    driver.implicitly_wait(10)

    # jumia popup is displayed
    popup = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "cw"))
    )
    close_btn = popup.find_element(By.CLASS_NAME, "cls")
    close_btn.click()

    # search for product
    search_bar = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "fi-q"))
    )
    search_bar.clear()
    search_bar.send_keys(product_name)
    search_bar.send_keys(Keys.RETURN)

    # # results are displayed
    results = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "section.card.-fh"))
    )
    return get_result_list(driver.page_source)
    