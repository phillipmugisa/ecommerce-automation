from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup as Bs

BASE_URL = "http://www.ebay.com"
options = Options()
options.headless = True

def parse_products(products_wrapper, layout):
    products = products_wrapper.find_all("li", attrs={"class": "s-item"})
    products_data = []
    for product in products:
        image = product.select('.s-item__image-wrapper img')[0].get('src', "None")
        price = product.find("span", attrs={"class": "s-item__price"}).getText()
        seller = product.find("span", attrs={"class": "s-item__seller-info-text"}).getText() if product.find("span", attrs={"class": "s-item__seller-info-text"}) else None

        url = product.select(".s-item__link")[0].get('href')
        name = product.select('.s-item__title [role="heading"]')[0].getText()

        product_data = {
            "image": image,
            "name": name,
            "url": url,
            "price": price,
            "seller": seller
        }
        products_data.append(product_data)
    return products_data
    

def get_result_list(page_source):
    soup = Bs(page_source, "html.parser")
    products_wrapper = soup.find("ul", attrs={"class": "srp-results"})
    if "srp-grid" in products_wrapper["class"]:
        return parse_products(products_wrapper, "srp-grid")
    return parse_products(products_wrapper, "srp-list")

def product_search(product_name):
    driver = webdriver.Chrome(options=options)
    driver.get(BASE_URL)
    # driver.implicitly_wait(10)

    # search for product
    search_bar = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "gh-ac"))
    )
    search_bar.clear()
    search_bar.send_keys(product_name)
    search_bar.send_keys(Keys.RETURN)

    # # results are displayed
    results = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".srp-results"))
    )
    return get_result_list(driver.page_source)
    