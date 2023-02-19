from decouple import config
import pymysql
from bs4 import BeautifulSoup
from selenium import webdriver
# from selenium.webdriver.firefox.options import Options
import time

# Read the settings from the .env file
HOST = config("HOST")
USER = config("USER")
PASSWORD = config("PASSWORD")
DATABASE = config("DATABASE")

# Open the website using Selenium
options = webdriver.FirefoxOptions()
options.add_argument("--headless")
driver = webdriver.Firefox(options=options)
driver.get("https://www.nepalstock.com.np/company/detail/131")

# Wait for the page to load
time.sleep(3)

# Extract the page source
html = driver.page_source

# Close the browser
driver.close()

# Use Beautiful Soup to parse the HTML
soup = BeautifulSoup(html, "html.parser")

# Extract the data you want to scrape
data = soup.find_all("td")

# Connect to Mysql
connection = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DATABASE)

# Insert the data into a Mysql table
try:
    with connection.cursor() as cursor:
        # Create the table(if it doesn't exist)
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS nepalstock(
                id INT NOT NULL AUTO_INCREMENT,
                data TEXT,
                PRIMARY KEY(id)
            )
        """
        )
        # Insert the data
        for item in data:
            sql = "INSERT INTO nepalstock(data) VALUES(%s)"
            cursor.execute(sql, (item.text,))

    # Commit the changes
    connection.commit()

finally:
    # close the connection
    connection.close()


# write the data to a Notepad file
# with open("data.txt", "w", encoding='utf-8') as file:
#     for item in data:
#         file.write(item.text)


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
