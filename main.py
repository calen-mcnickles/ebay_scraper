from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import re
from user_ag import user_agent_DF # DF made via a CSV file from https://developers.whatismybrowser.com/useragents/database/
import random
import time

"""
Ebay Scraper that will pull desired product searches from CSV - 

Outputs to CSV - 
    Listing Title
    Price
    Shipping Cost
    Time left on listing
    Listing link
"""

path = r"C:\Users\..."

# Turns keywords into url format
def searchify(keywords):
    keywords = keywords.split()
    new_keyword = ""
    for word in keywords:
        new_keyword += word + "+"
    new_keyword = new_keyword[:-1]
    return new_keyword


class EbayScraper:
    def __init__(self, keyword, max_price, is_sold: bool):
        self.keyword = keyword
        self.max_price = max_price
        searchified_keyword = searchify(keyword)
        if is_sold is True:
            self.search_url = "https://www.ebay.com/sch/i.html?_nkw=" + searchified_keyword + "&LH_Sold=1&LH_Complete=1"
        else:
            self.search_url = "https://www.ebay.com/sch/i.html?_nkw=" + searchified_keyword + "&rt=nc&_udhi=" + str(
                max_price)

    def scrape_active_pages(self, pages_to_search):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) '
                                 'Chrome/80.0.3987.132 Safari/537.36'}

        product_list = []
        # Loops through pages to search
        for i in range(1, pages_to_search + 1):
            try:
                search_multiple_page = self.search_url + "&_pgn=" + str(i)
                result = requests.get(search_multiple_page, headers=headers, timeout=5)
                soup = bs(result.content, "html.parser")
                products = soup.find_all("div", class_="s-item__wrapper clearfix")
            except requests.exceptions.Timeout:
                continue
            for item in products:
                name = item.h3.text
                link = item.find_all("a", {"href": re.compile("^https://www.ebay.com/itm/")})
                price = item.find_all("span", class_="s-item__price")
                shipping_cost = item.find_all("span", class_="s-item__shipping s-item__logisticsCost")
                time_left = item.find_all("span", class_="s-item__time-left")
                # end_date = item.find_all("span", class_="s-item__time-end") # Maybe get end date later on. BS doesnt seems to be able to locate the text

                price_1 = 0
                shipping = ""
                time_l = ""
                for p in price:
                    price_1 = p.text
                for li in link:
                    link_s = li.get('href')
                for sh in shipping_cost:
                    shipping = sh.text.replace("shipping", "")
                for t_l in time_left:
                    time_l = t_l.text

                product_list.append({
                    "Keyword": self.keyword,
                    "Posting Title": name,
                    "Price": price_1,
                    "Shipping Cost": shipping,
                    "Total Cost": "",  # sum price and shipping
                    "Time Left": time_l,
                    "Link": link_s
                })
        return product_list

    def scrape_sold_pages(self, pages_to_search):
        product_list = []
        # Loops through pages to search
        for i in range(1, pages_to_search + 1):
            # Creates random header using list of User-Agents. Will try different headers until one works.
            not_scraped = True
            while not_scraped:
                headers = {"User-Agent": user_agent_DF["user_agent"][random.randint(0, len(user_agent_list))]}
                print(headers) # Testing
                try:
                    search_multiple_page = self.search_url + "&_pgn=" + str(i)
                    result = requests.get(search_multiple_page, headers=headers, timeout=5)
                    soup = bs(result.content, "html.parser")
                    products = soup.find_all("div", class_="s-item__wrapper clearfix")
                except requests.exceptions.Timeout or requests.exceptions.ConnectionError:
                    continue
                not_scraped = False

            for item in products:
                name = item.h3.text
                link = item.find_all("a", {"href": re.compile("^https://www.ebay.com/itm/")})
                price = item.find_all("span", class_="s-item__price")
                shipping_cost = item.find_all("span", class_="s-item__shipping s-item__logisticsCost")

                price_1 = 0
                shipping = ""
                for p in price:
                    price_1 = p.text
                for li in link:
                    link_s = li.get('href')
                for sh in shipping_cost:
                    shipping = sh.text.replace("shipping", "")

                product_list.append({
                    "Keyword": self.keyword,
                    "Posting Title": name,
                    "Price": price_1,
                    "Shipping Cost": shipping,
                    "Total Cost": "",  # sum price and shipping
                    "Link": link_s
                })
        return product_list


def ebay_scraper(export_name, file_name, pages_to_scrape, is_sold: bool):
    # Reads from csv list of items needed and the max price
    products_df = pd.DataFrame(pd.read_csv(path+"\\"+file_name))
    df_list = []
    # if is_sold is true run scraper for sold items
    if is_sold is True:
        for i in range(len(products_df)):
            x = EbayScraper(products_df.iloc[i][0], products_df.iloc[i][1], is_sold)
            print(x.search_url)
            df = pd.DataFrame(x.scrape_sold_pages(pages_to_scrape))
            # print(df)
            df_list.append(df)
            time.sleep(1)

    # Runs ebay scraper for each card in the CSV document
    else:
        for i in range(len(products_df)):
            x = EbayScraper(products_df.iloc[i][0], products_df.iloc[i][1], is_sold)
            print(x.search_url)
            df = pd.DataFrame(x.scrape_active_pages(pages_to_scrape))
            # print(df)
            df_list.append(df)
            time.sleep(1)

    result = pd.concat(df_list)
    result.to_csv(path + "\\" + export_name)


# Calling Ebay scraper functions
ebay_scraper("Pokemon_card_list_active.csv", "Missing Pokemon cards.csv", 2, False)

ebay_scraper("Pokemon_card_list_sold.csv", "Missing Pokemon cards.csv", 1, True)





