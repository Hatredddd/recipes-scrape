import requests
from bs4 import BeautifulSoup
import lxml
import os
import time
import json
from _datetime import datetime
import csv


# ====================================STEP 1:We save the HTML template of the main page in order to continue working through it.=================================
# ----------------------------------------------------START--------------------------------------------------------------------------------------------------------
def get_all_pages():
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    }
    r = requests.get(url='https://luch.by/watches/muzhskie/', headers=headers)
    if not os.path.exists('data'):
        os.mkdir('data')
    with open('data/page_1.html', 'w', encoding='utf-8') as file:
        file.write(r.text)

    # ----------------------------------------------------END--------------------------------------------------------------------------------------------------------

    # ====================================STEP 2:We find and save the templates of all pages of the product we need.=================================

    with open('data/page_1.html', encoding='utf-8') as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')
    pages_count = int(soup.find('div', class_='pagination').find_all('a')[-2].text)

    for i in range(1, pages_count + 1):
        url = f'https://luch.by/watches/filter/product_type-is-pt2/apply/?PAGEN_1={i}'
        r = requests.get(url=url, headers=headers)
        with open(f'data/page_{i}.html', 'w', encoding='utf-8') as file:
            file.write(r.text)

        time.sleep(3)
    return pages_count + 1


# ----------------------------------------------------END--------------------------------------------------------------------------------------------------------


# ====================================STEP 3:We create a csv file, create a cycle for collecting the necessary data and supplement csv.=================================

def collect_data(pages_count):
    date_time = datetime.now().strftime('%d_%m_%Y')

    with open(f'data_{date_time}.csv', 'w') as file:
        writer = csv.writer(file)

        writer.writerow(
            (
                'Article',
                'Price',
                'URL'
            )
        )
    data = []
    for page in range(1, pages_count):
        with open(f'data/page_{page}.html', encoding='utf-8') as file:
            src = file.read()

        soup = BeautifulSoup(src, 'lxml')
        items_cards = soup.find_all('a', class_='block__link')

        for item in items_cards:
            product_article = item.find('div', class_='article').text
            product_price = item.find('div', class_='price').text
            product_url = f'https://luch.by{item.get("href")}'

            data.append(
                {
                    'product_article': product_article,
                    'product_price': product_price,
                    'product_url': product_url
                }
            )

            with open(f'data_{date_time}.csv', 'a') as file:
                writer = csv.writer(file)

                writer.writerow(
                    (
                        product_article,
                        product_price.strip(),
                        product_url
                    )
                )

    with open(f'data_{date_time}.json', 'a', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


# ----------------------------------------------------END--------------------------------------------------------------------------------------------------------


def main():
    pages_count = get_all_pages()
    collect_data(pages_count=pages_count)


if __name__ == '__main__':
    main()