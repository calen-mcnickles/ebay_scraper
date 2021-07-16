from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import re

"""
Ebay Scraper that will pull desired product searches from CSV - 

Outputs to CSV - 
    Listing Title
    Price
    Shipping Cost
    Time left on listing
    Listing link
"""

# Turns keywords into url format
def searchify(keywords):
    keywords = keywords.split()
    new_keyword = ""
    for word in keywords:
        new_keyword += word + "+"
    new_keyword = new_keyword[:-1]
    return new_keyword


class EbayScraper:
    def __init__(self, keyword, max_price):
        self.keyword = keyword
        self.max_price = max_price
        searchified_keyword = searchify(keyword)
        self.search_url = "https://www.ebay.com/sch/i.html?_nkw=" + searchified_keyword + "&rt=nc&_udhi=" + str(
            max_price)

    def scrape_pages(self, pages_to_search):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) '
                                 'Chrome/80.0.3987.132 Safari/537.36'}
        product_list = []
        # Loops through pages to search
        for i in range(1, pages_to_search + 1):
            search_multiple_page = self.search_url + "&_pgn=" + str(i)
            result = requests.get(search_multiple_page, headers=headers)
            soup = bs(result.content, "html.parser")
            products = soup.find_all("div", class_="s-item__wrapper clearfix")
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
                    "Total Cost": "",  # blank for now. Eventually sum price and shipping
                    "Time Left": time_l,
                    "Link": link_s
                })
        return product_list


def ebay_scraper(export_name, file_name, pages_to_scrape):
    # Reads from csv list of items needed and the max price
    products_df = pd.DataFrame(pd.read_csv(file_name))

    # Runs ebay scraper for each card in the CSV document
    df_list = []
    for i in range(len(products_df)):
        x = EbayScraper(products_df.iloc[i][0], products_df.iloc[i][1])
        df = pd.DataFrame(x.scrape_pages(pages_to_scrape))
        df_list.append(df)

    result = pd.concat(df_list)
    print(result)

    result.to_csv(export_name)

# Scrapes 1 page of listings, pulling keywords from "Missing Pokemon Cards.csv" and exporting to "Pokemon_card_list.csv"
ebay_scraper("Pokemon_card_list.csv", "Missing Pokemon cards.csv", 1)




