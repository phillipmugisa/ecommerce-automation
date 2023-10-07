from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup as Bs

BASE_URL = "http://www.amazon.com"
options = Options()
options.headless = True

# gird = sg-col-4-of-24 sg-col-4-of-12 sg-col-4-of-16 sg-col-4-of-20
# row = sg-col-20-of-24 sg-col-0-of-12 sg-col-16-of-20 sg-col-12-of-16

def parse_products(products):
    products_data = []
    for product in products:
        url = product.select('[data-component-type="s-product-image"] .a-link-normal')[0].get('href', "None")
        image = product.select('[data-component-type="s-product-image"] .s-image')[0].get('src', "None")

        # check if product layout is grid or rows
        if "sg-col-4-of-24" in product["class"]:
            name = product.find("div", attrs={"class": "puis-padding-right-small"}).find("span", attrs={"class": "a-size-base-plus a-color-base a-text-normal"}).getText()
            price = product.select('span.a-price span.a-offscreen')[0].getText() if product.select('span.a-price span.a-offscreen') else None
            
            # product has price range
            if product.find("span", attrs={"class": "a-price-dash"}) and price:
                price = f"{price} - {product.select('span.a-price span.a-offscreen')[1].getText()}"
        else:
            name = product.find("div", attrs={"class": "s-list-col-right"}).find("span", attrs={"class": "a-size-medium a-color-base a-text-normal"}).getText()
            price = product.select('span.a-price span.a-offscreen')[0].getText() if product.select('span.a-price span.a-offscreen') else None

        product_data = {
            "name": name,
            "url": f"{BASE_URL}{url}",
            "image": image,
            "price": price
        }
        products_data.append(product_data)
    return products_data
    

def get_result_list(page_source):
    soup = Bs(page_source, "html.parser")
    products = soup.find_all(attrs = {'data-component-type':"s-search-result"})
    return parse_products(products)


def product_search(product_name):
    driver = webdriver.Chrome(options=options)
    driver.get(BASE_URL)
    # driver.implicitly_wait(10)

    # search for product
    search_bar = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "twotabsearchtextbox"))
    )
    search_bar.clear()
    search_bar.send_keys(product_name)
    search_bar.send_keys(Keys.RETURN)

    # # results are displayed
    results = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-component-type='s-search-result']"))
    )
    return get_result_list(driver.page_source)
    