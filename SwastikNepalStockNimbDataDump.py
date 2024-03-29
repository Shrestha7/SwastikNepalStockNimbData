import os
import time
from decouple import config
from fake_useragent import UserAgent
import pymysql
from bs4 import BeautifulSoup
from selenium import webdriver

# Read the settings from the .env file
HOST = config("HOST", default="localhost")
USER = config("USER")
PASSWORD = config("PASSWORD")
DATABASE = config("DATABASE")
table_name = config("TABLE_NAME", cast=str)
sleep_time = config("SLEEP_TIME", cast=int)
url_value = config("URL", cast=str)


# Generate a random user agent
# Help to mimic the behavior of real web browser and 
# prevent websites from detecting the scraper and blocking it.
ua = UserAgent()
headers = {"User-Agent": ua.random}


# Open the website using Selenium
# Use FirefoxOptions to open the browser in headless mode
options = webdriver.FirefoxOptions()
options.add_argument("--headless")
options.add_argument("--log-level=0")
options.add_argument('--disable-gpu')
driver = webdriver.Firefox(options=options)
driver.header_overrides = headers
driver.get(url_value)

# Wait for the page to load
time.sleep(sleep_time)

# Extract the page source
html = driver.page_source

# Close the browser
driver.close()

# Use Beautiful Soup to parse the HTML
soup = BeautifulSoup(html, "html.parser")

# Extract the data you want to scrape
#Find all the td tags inside table tags and extract the text content
# data = soup.find_all("td")
data = soup.select("table.table tr td")[0:13]
# print(data[::])
# Connect to Mysql
connection = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DATABASE)

# Insert the data into a Mysql table
try:
    with connection.cursor() as cursor:
        # Create the table(if it doesn't exist)
        # cursor.execute(
        #     """
        #     CREATE TABLE IF NOT EXISTS nepalstock(
        #         id INT NOT NULL AUTO_INCREMENT,
        #         created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        #         instrument_type TEXT,
        #         listing_date TEXT,
        #         last_tradedprice TEXT,
        #         total_traded_quantity TEXT,
        #         total_trades TEXT,
        #         previous_day_closeprice TEXT,
        #         price TEXT,
        #         weeks52 TEXT,
        #         openPrice TEXT,
        #         closeprice TEXT,
        #         total_listedShares TEXT,
        #         total_paidupvalues TEXT,
        #         marketcapitalization TEXT,
        #         note TEXT,
        #         PRIMARY KEY(id)
        #     )
        # """
        # )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS {}(
                id INT NOT NULL AUTO_INCREMENT,
                AsOfDate DATETIME DEFAULT CURRENT_TIMESTAMP,
                InstrumentType TEXT,
                ListingDate TEXT ,
                LastTradedPrice TEXT,
                TotalTradedQuantity TEXT ,
                TotalTrades TEXT ,
                PreviousDayClosePrice TEXT ,
                HighPriceLowPrice TEXT , 
                52WeekHigh52WeekLow TEXT ,
                OpenPrice TEXT ,
                ClosePrice TEXT ,
                TotalListedShares TEXT ,
                TotalPaidupValue TEXT ,
                MarketCapitalization TEXT,
                PRIMARY KEY(id)
            )
            """.format(table_name)
            
        )
        
        # row = [item.text for item in data]
        # creates a list of 14 elements called row.
        # check if <td> tag if condtion
        # if td tag then gets text and remove whitespaces due to strip = true.
        
        row = [
            item.get_text(strip=True).replace(",", "")
            for item in data
            if item.name == "td"
        ]
        # print(row)
        # check row list= 14, if !=14 raises valueerror.
        # to ensure the data is scraped correctly,
        # to prevent incorrect data from being inserted into database.
        if len(row) != 13:
            raise ValueError("Expected 13 items in row, got %d" % len(row))
        # Insert the data
        # sql = """
        #     INSERT INTO nepalstock(
        #         instrument_type,
        #         listing_date ,
        #         last_tradedprice ,
        #         total_traded_quantity ,
        #         total_trades ,
        #         previous_day_closeprice ,
        #         price ,
        #         weeks52 ,
        #         openPrice ,
        #         closeprice ,
        #         total_listedShares ,
        #         total_paidupvalues ,
        #         marketcapitalization,
        #         note
                
        #     ) VALUES(
        #         %s,%s,%s,%s,%s,%s,%s,
        #         %s,%s,%s,%s,%s,%s,%s
        #     )
        # """

        sql= f"""
            INSERT INTO {table_name}(
            InstrumentType ,
            ListingDate ,
            LastTradedPrice,
            TotalTradedQuantity ,
            TotalTrades ,
            PreviousDayClosePrice ,
            HighPriceLowPrice , 
            52WeekHigh52WeekLow ,
            OpenPrice ,
            ClosePrice ,
            TotalListedShares ,
            TotalPaidupValue ,
            MarketCapitalization
            )
            Values(
                %s,%s,%s,%s,%s,%s,%s,
                %s,%s,%s,%s,%s,%s
            )
        """
        # inserts the data stored in the row list
        # into the corresponding columns of the table
        # in the database.
        # tuple function used to convert row list into tuple.
        cursor.execute(sql, tuple(row))
        # Commit the changes
        connection.commit()


finally:
    # close the connection
    connection.close()

# os.system("taskkill /f /im geckodriver.exe")
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
