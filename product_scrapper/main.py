from amazon import product_search as amazon_scrapper
from ebay import product_search as ebay_scrapper
from jumia import product_search as jumia_scrapper

def get_products(product_name, platform):
    if platform.lower() == "Amazon".lower():
        return {
            "platform": platform,
            "products" : amazon_scrapper.product_search(product_name)
        }
    elif platform.lower() == "Ebay".lower():
        return {
            "platform": platform,
            "products" : ebay_scrapper.product_search(product_name)
        }
    elif platform.lower() == "Jumia".lower():
        return {
            "platform": platform,
            "products" : jumia_scrapper.product_search(product_name)
        }

def main():
    platform = input("Choose your platform (All, Amazon, Ebay, Jumia): ")
    prompt = input("Enter Product Name: ")

    products = get_products(prompt, platform.lower())
    print(products)

if __name__ == "__main__":
    main()