import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver

def main():


    #Creates headers that bypass the webscraper / bot blockers
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}
    #Asks user for search criteria and replaces the space with +
    search = input("Search: ")
    #search.replace(" ", "+")

    URL = f"https://www.jmbullion.com/search/?q={search}"
    page = requests.get(URL, headers=headers)

    driver = webdriver.Chrome()
    driver.get(URL)
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    bullion = soup.find_all("div", class_="product type-product status-publish hentry mainproductIn cat-product first instock")
    
    with open('yourfile.html', 'w') as f:
        f.write(str(bullion))
    
    for bull in bullion:
        title = bull.find("span", class_="title")
        price = bull.find("span", class_="price")
        print(title)
        print(price)

main()