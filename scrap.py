import requests
from bs4 import BeautifulSoup
from lxml import html
from urllib import parse

URL = None
supported_sites = ['www.amazon.com', 'www.flipkart.com']
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
}

def get_url_from_user():
    URL = input(
        'Please enter the URL for the product from the website:')
    parsed_url = parse.urlsplit(URL)
    response = requests.get(URL, headers=HEADERS)
    html_response = BeautifulSoup(response.content, 'lxml')
    if parsed_url.netloc == 'www.amazon.com':
        current_price = html_response.find(
            'span', {'id':'priceblock_ourprice'}).get_text()
    elif parsed_url.netloc == 'www.flipkart.com':
        current_price = html_response.select('div._1vC4OE._3qQ9m1')
        current_price = current_price[0].get_text()
    elif parsed_url.netloc == 'www.snapdeal.com':
        for sub_div in html_response.select('span.pdp-final-price'):
            current_price = sub_div.findAll('span', {'class':'payBlkBig'})
            current_price = current_price[0].get_text()
    else:
        print('None of the above')
    return current_price

if __name__ == '__main__':
    print(get_url_from_user())