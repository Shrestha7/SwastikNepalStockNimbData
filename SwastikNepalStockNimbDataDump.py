import time
from decouple import config

import pymysql
from bs4 import BeautifulSoup
from selenium import webdriver

# Read the settings from the .env file
HOST = config("HOST", default="localhost")
USER = config("USER")
PASSWORD = config("PASSWORD")
DATABASE = config("DATABASE")

# Open the website using Selenium
options = webdriver.FirefoxOptions()
options.add_argument("--headless")
driver = webdriver.Firefox(options=options)
driver.get("https://www.nepalstock.com.np/company/detail/132")

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
print(data)
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
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                instrument_type TEXT,
                listing_date TEXT,
                last_tradedprice TEXT,
                total_traded_quantity TEXT,
                total_trades TEXT,
                previous_day_closeprice TEXT,
                price TEXT,
                weeks52 TEXT,
                openPrice TEXT,
                closeprice TEXT,
                total_listedShares TEXT,
                total_paidupvalues TEXT,
                marketcapitalization TEXT,
                note TEXT,
                promoter_shares TEXT,
                public_shares TEXT,
                total_listed_shares TEXT,
                PRIMARY KEY(id)
            )
        """
        )
        # Insert the data
        row = [item.text for item in data]
        sql = """
            INSERT INTO nepalstock(
                instrument_type,
                listing_date ,
                last_tradedprice ,
                total_traded_quantity ,
                total_trades ,
                previous_day_closeprice ,
                price ,
                weeks52 ,
                openPrice ,
                closeprice ,
                total_listedShares ,
                total_paidupvalues ,
                marketcapitalization,
                note ,
                promoter_shares,
                public_shares ,
                total_listed_shares 
            ) VALUES(
                %s,%s,%s,%s,%s,%s,%s,
                %s,%s,%s,%s,%s,%s,%s,%s,%s,%s
            )
        """

        cursor.execute(sql, tuple(row))
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
