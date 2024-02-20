"""
create search function
Get desired information from websites,
safe data to csv file,
use data to show information and links to websites
sort by price
"""
import csv
import requests
from bs4 import BeautifulSoup

# URL of the webpage to scrape
url = 'https://airbnb.com'

# Send an HTTP request to the webpage
response = requests.get(url)

# Parse the HTML content
soup = BeautifulSoup(response.text, 'html.parser')

# Extract all text from the webpage
all_text = soup.get_text(separator='\n', strip=True)

# Write the extracted data into a CSV file
csv_file = 'scraped_data.csv'
with open(csv_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Text'])  # header
    writer.writerow([all_text])

print(f"Data has been scraped and saved to '{csv_file}'")
