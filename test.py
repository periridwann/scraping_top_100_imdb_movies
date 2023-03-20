import unittest
from bs4 import BeautifulSoup
import requests
import mysql.connector

class TestIMDBScraper(unittest.TestCase):

    def test_imdb_scraper(self):
        base_url = 'https://www.imdb.com/search/title/?groups=top_100&ref_=adv_prv'
        list = []

        for page_num in range(1, 3):
            url = f'{base_url}&start={((page_num - 1) * 50) + 1}'
            response = requests.get(url)
            data = BeautifulSoup(response.text, 'html.parser')

            for area in data.find_all('div',class_="lister-item mode-advanced"):
                title = area.find('h3').find('a').get_text()
                year = area.find('span',class_='lister-item-year text-muted unbold').get_text().replace('(I) ', '').replace('(', '').replace(')', '')
                runtime = area.find('span',class_='runtime').get_text().replace(' min', '')
                genre = area.find('span',class_='genre').get_text()
                rating = area.find('strong').get_text()

                list.append((title, year, runtime, genre, rating))

                # --------- SAVE TO MYSQL ----------
                cnx = mysql.connector.connect(user='root', database='movies')
                cursor = cnx.cursor()

                add = ("INSERT INTO imdb "
                            "(title, year, runtime, genre, rating) "
                            "VALUES (%s, %s, %s, %s, %s)")

                item = (title, year, runtime, genre, rating)
                cursor.execute(add, item)
                emp_no = cursor.lastrowid
                cnx.commit()
                cursor.close()
                cnx.close()

        self.assertEqual(len(list), 100) # check if 100 records are scraped
        # you can also add more assertions to check the values of the scraped data

if __name__ == '__main__':
    unittest.main()
