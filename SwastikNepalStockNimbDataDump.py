from bs4 import BeautifulSoup
from selenium import webdriver
import time


# Open the website using Selenium
driver = webdriver.Firefox()
driver.get("https://www.nepalstock.com.np/company/detail/131")

# Wait for the page to load
time.sleep(3)

# Extract the page source
html = driver.page_source

# Close the browser
driver.close()

# Use Beautiful Soup to parse the HTML
soup = BeautifulSoup(html, 'html.parser')

# Extract the data you want to scrape
data = soup.find_all("td")

# write the data to a Notepad file
with open("data.txt", "w", encoding='utf-8') as file:
    for item in data:
        file.write(item.text)







# driver = webdriver.Firefox()
# driver.get("https://www.nepalstock.com.np/company/detail/131")
# html = driver.page_source
# soup = BeautifulSoup(html, 'html.parser')
# data = soup.find_all('table', {'class': 'table'})

# print (data)
# driver.close()

# file = open("data.txt", "w")
# file.write(data)
# file.close()
