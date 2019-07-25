import requests
from bs4 import BeautifulSoup
from lxml import html
from urllib import parse
import math
import json


class Scraper:

    def __init__(self, URL):
        self.current_price = None
        self.actual_price = None
        self.deal_price = None
        self.discount = None
        self.URL = URL
        self.HEADERS = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }

    def get_url_from_user(self):
        try:
            parsed_url = parse.urlsplit(self.URL)
            response = requests.get(self.URL, headers=self.HEADERS)
            html_response = BeautifulSoup(response.content, 'lxml')
            if parsed_url.netloc == 'www.amazon.com' or parsed_url.netloc == 'www.amazon.in':
                return self.scrap_amazon(html_response)
            elif parsed_url.netloc == 'www.flipkart.com':
                return self.scrap_flipkart(html_response)
            elif parsed_url.netloc == 'www.snapdeal.com':
                return self.scrap_snapdeal(html_response)
            else:
                print('None of the above')
        except AttributeError as error:
            print(error)

    def scrap_amazon(self, html_response):
        product_image = None
        # get product image
        try:
            product_image = html_response.select_one('img#landingImage')[
                'data-a-dynamic-image']
            product_image = list(json.loads(product_image).keys())[0]
        except:
            product_image = 'NA'
        # get actual price
        try:
            self.actual_price = html_response.select_one(
                'span.priceBlockStrikePriceString.a-text-strike').get_text()
            self.actual_price = float(self.actual_price.strip().replace(
                '₹', '').replace(',', '').replace('$', ''))
        except AttributeError as error:
            self.actual_price = 'NA'
        # get current price
        try:
            self.current_price = html_response.select_one(
                'span#priceblock_ourprice').get_text()
            self.current_price = float(self.current_price.strip().replace(
                '₹', '').replace(',', '').replace('$', ''))
        except AttributeError as error:
            self.current_price = 'NA'
        # get deal price
        try:
            self.deal_price = html_response.select_one(
                'span#priceblock_dealprice').get_text()
            self.deal_price = float(self.deal_price.strip().replace(
                '₹', '').replace(',', '').replace('$', ''))
        except AttributeError as error:
            self.deal_price = 'NA'
        if self.current_price == 'NA' and self.deal_price != 'NA':
            self.current_price = self.deal_price
        elif self.current_price == 'NA' and self.deal_price == 'NA':
            self.current_price = self.actual_price
        elif self.actual_price == 'NA' and self.current_price != 'NA':
            self.actual_price = self.current_price
        discount = math.floor(
            ((self.actual_price - self.current_price) / self.actual_price) * 100)
        return {
            'product_image': product_image,
            'actual_price': self.actual_price,
            'current_price': self.current_price,
            'discount': discount
        }

    def scrap_flipkart(self, html_response):
        # get produc image
        product_image = 'https://www.wileyindia.com/pub/static/frontend/Magento/luma/en_US/images/Flipkart.jpg'
        # get actual price
        try:
            self.actual_price = html_response.select_one(
                'div._3auQ3N._1POkHg').get_text().strip()
            self.actual_price = float(self.actual_price.replace('₹', '').replace(',', ''))
        except AttributeError as error:
            self.actual_price = 'NA'
        # get current price
        try:
            self.current_price = html_response.select_one(
                'div._1vC4OE._3qQ9m1').get_text().strip()
            self.current_price = float(self.current_price.replace('₹', '').replace(',', ''))
        except AttributeError as error:
            self.current_price = 'NA'
        if self.actual_price == 'NA' and self.current_price != 'NA':
            self.actual_price = self.current_price
        elif self.actual_price != 'NA' and self.current_price == 'NA':
            self.current_price = self.actual_price
        discount = math.floor(((self.actual_price - self.current_price)/self.actual_price) * 100)
        return {
            'product_image': product_image,
            'actual_price': self.actual_price,
            'current_price': self.current_price,
            'discount': discount
        }

    def scrap_snapdeal(self, html_response):
        # get product image
        try:
            img_container = html_response.select_one('ul#bx-slider-left-image-panel')
            product_image = img_container.select('img.cloudzoom')[0]['src']
        except:
            product_image = 'NA'
        # get actual price
        try:
            self.actual_price = html_response.select_one(
                'div.pdpCutPrice').get_text().strip()
            self.actual_price = float(self.actual_price[9:15].replace(',', ''))
        except AttributeError as error:
            self.actual_price = 'NA'
        # get current price
        try:
            for sub_div in html_response.select('span.pdp-final-price'):
                self.current_price = sub_div.find(
                    'span', {'class': 'payBlkBig'}).get_text().strip()
                self.current_price = float(self.current_price)
        except AttributeError as error:
            self.current_price = 'NA'
        if self.actual_price == 'NA' and self.current_price != 'NA':
            self.actual_price = self.current_price
        elif self.actual_price != 'NA' and self.current_price == 'NA':
            self.current_price = self.actual_price
        discount = math.floor(((self.actual_price - self.current_price)/self.actual_price) * 100)
        return {
            'product_image': product_image,
            'actual_price': self.actual_price,
            'current_price': self.current_price,
            'discount': discount
        }


if __name__ == '__main__':
    scraper = Scraper()
    scraper.get_url_from_user()
