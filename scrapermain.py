import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from pyvirtualdisplay import Display
import time


class BaseScraper:
    def __init__(self, search_query):
        self.search_query = search_query

    def get_url(self):
        raise NotImplementedError("Subclasses must implement get_url method")

    def scrape(self):
        raise NotImplementedError("Subclasses must implement scrape method")


class JMBullionScraper(BaseScraper):
    def get_url(self):
        # Directly redirect to the search URL after reaching the homepage
        return f"https://www.jmbullion.com/search/?q={self.search_query}"

    def scrape(self):
        display = Display(visible=0, size=(800, 600))#Change visibility to '1' to view window.
        display.start()

        try:
            home_url = "https://www.jmbullion.com/"
            driver = webdriver.Chrome()
            driver.get(home_url)
            # Immediately redirect to the search URL(NEEDED TO BYPASS 403err, PROXY AND HEADERS DON'T WORK)
            driver.get(self.get_url())
            #time.sleep(5)  # Add a delay to allow the search results to load
            soup = BeautifulSoup(driver.page_source, "html.parser")
            driver.quit()

            products = soup.find_all("div", class_="product type-product status-publish hentry mainproductIn cat-product first instock")
            results = []
            for product in products:
                title = product.find("span", class_="title")
                price = product.find("span", class_="price")
                link = product.find("a", href=True)['href'] if product.find("a", href=True) else None
                image_tag = product.find("img")
                image = image_tag['src'] if image_tag else None
                if title and price and link:
                    result = {
                        'title': title.text.strip(),
                        'price': price.text.strip(),
                        'link': link
                    }
                    if image:
                        result['image'] = image
                    results.append(result)
        finally:
            display.stop()

        return results



class APMEXScraper(BaseScraper):
    def get_url(self):
        return f"https://www.apmex.com/search?&q={self.search_query}"

    def scrape(self):
        display = Display(visible=1, size=(800, 600))#Makes new window sneaky
        display.start()

        try:
            URL = self.get_url()
            driver = webdriver.Chrome()
            driver.get(URL)
            soup = BeautifulSoup(driver.page_source, "html.parser")
            driver.quit()

            products = soup.find_all("div", class_="product-essential")
            results = []
            for product in products:
                title = product.find("div", class_="mod-product-title")
                price = product.find("span", class_="price")
                link = product.find("a", class_="item-link")['href'] if product.find("a", class_="item-link") else None
                link = ("https://www.apmex.com/" + link) #Add the appropriate prefix from extracted incomplete link.
                imagetag = product.find("img", class_="lazy")
                image = imagetag["src"] if imagetag else None
                if title and price and link:
                    result = {
                        'title': title.text.strip(),
                        'price': price.text.strip(),
                        'link': link
                    }
                    if image:  # Check if image exists before adding it to the result dictionary (DO NOT MESS WITH FOR DICT REASONS)
                        result['image'] = image
                    results.append(result)
        finally:
            display.stop()

        return results


def main():
    search_query = input("Enter search query for bullion and coin websites: ")

    # Configure scraper classes
    scraper_classes = {
        'jmbullion': JMBullionScraper,
        'apmex': APMEXScraper,
        # Add more scraper classes for additional websites
    }

    for website, scraper_class in scraper_classes.items():
        print(f"Scraping results from {website}...")
        scraper = scraper_class(search_query)
        results = scraper.scrape()
        if results:
            for result in results:
                print("Title:", result['title'])
                print("Price:", result['price'])
                print("Link:", result['link'])
                if 'image' in result:  # Check if 'image' key exists in the result dictionary
                    print("Image:", result['image'])
                else:
                    print("Image: Not available")  # Print a message if 'image' is not available
                print()
        else:
            print("No results found.")


if __name__ == "__main__":
    main()
