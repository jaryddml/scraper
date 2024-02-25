import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from flask import Flask, render_template, request


def main():

    #Creates headers that bypass the webscraper / bot blockers
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}
    #Asks user for search criteria and replaces the space with +
    search = input("Search: ")

    URL = f"https://www.jmbullion.com/search/?q={search}"
    page = requests.get(URL, headers=headers)

    driver = webdriver.Chrome()
    driver.get(URL)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    products = soup.find_all("div", class_="product type-product status-publish hentry mainproductIn cat-product first instock")
    
    #with open('yourfile.html', 'w') as f:
        #f.write(str(soup))
    
    for product in products:
        title = product.find("span", class_="title")
        price = product.find("span", class_="price")
        link = product.find("a", href=True)['href'] if product.find("a", href=True) else None
        if title:
            print("Title:", title.text.strip())
        if price:
            print("Price:", price.text.strip())
        if link:
            print("Link:", link)
        print()  # Just for spacing between entries

    driver.quit()

main()