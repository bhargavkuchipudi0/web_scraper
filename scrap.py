import requests
from bs4 import BeautifulSoup
from lxml import html
from urllib import parse


class Scraper:

    def __init__(self):
        self.current_price = None
        self.actual_price = None
        self.discount = None
        self.URL = None
        self.HEADERS = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }

    def scrap_amazon(self, html_response):
        try:
            self.actual_price = html_response.select_one('span.priceBlockStrikePriceString.a-text-strike').get_text()
            print(self.actual_price.strip())
        except AttributeError:
            print('Actual price not available')
        try:
            self.current_price = html_response.find(
            'span', {'id': 'priceblock_ourprice'}).get_text()
            print(self.current_price.strip())
        except AttributeError as error:
            print('Current price not available')

    def scrap_flipkart(self, html_response):
        try:
            self.actual_price = html_response.select_one('div._3auQ3N._1POkHg').get_text()
            print(self.actual_price.strip())
        except AttributeError as error:
            print('Actual price not available')    
        try:
            self.current_price = html_response.select_one('div._1vC4OE._3qQ9m1').get_text()
            print(self.current_price.strip())
        except AttributeError as error:
            print('Current price not available')

    def scrap_snapdeal(self, html_response):
        try:
            for ele in html_response.select('div.normalText'):
                ele.decompose()
            self.actual_price = html_response.select_one('div.pdpCutPrice ')
            print(self.actual_price.get_text().strip())
        except AttributeError as error:
            print(error)
            print('Actual price not available')
        try:
            for sub_div in html_response.select('span.pdp-final-price'):
                self.current_price = sub_div.find(
                    'span', {'class': 'payBlkBig'}).get_text()
            print(self.current_price.strip())
        except AttributeError as error:
            print('Current price not available')

    def get_url_from_user(self):
        try:
            self.URL = input(
                'Please enter the URL for the product from the website:')
            parsed_url = parse.urlsplit(self.URL)
            response = requests.get(self.URL, headers=self.HEADERS)
            html_response = BeautifulSoup(response.content, 'lxml')
            if parsed_url.netloc == 'www.amazon.com' or parsed_url.netloc == 'www.amazon.in' :
                self.scrap_amazon(html_response)
            elif parsed_url.netloc == 'www.flipkart.com':
                self.scrap_flipkart(html_response)
            elif parsed_url.netloc == 'www.snapdeal.com':
                self.scrap_snapdeal(html_response)
            else:
                print('None of the above')
        except AttributeError as error:
            print(error)


if __name__ == '__main__':
    scraper = Scraper()
    scraper.get_url_from_user()
