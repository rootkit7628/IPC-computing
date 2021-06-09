import requests
from bs4 import BeautifulSoup

import mysql.connector

Database = {
	'Host' : '',
	'Database' : '',
	'User' : '',
	'Password' : ''
}

class IPC():

	def __init__(self):
		self.db = mysql.connector.connect(**Database)
		self.cursor = self.db.cursor()

	def insert_article():
		query = '''
			INSERT IGNORE INTO 
				Produits(name, url, image, prix, categorie, marque, description)
			VALUES
				(%s, %s, %s, %s, %s, %s, %s, %s)

		'''

		self.cursor.execute(query, (name, url, image, prix, categorie, marque, description))

	def get_categorie():

		url = 'https://www.ipc-computer.fr/'

		categorie = {}

		r = requests.get('https://www.ipc-computer.fr/notebook-kategorien')

		src_code = BeautifulSoup(r.text, 'html.parser')

		for a in src_code.find_all('a'):
			link = a.get('href')
			if link.startswith('/pieces-detachees/'):
				categorie_name = a.get('title')
				categorie_link = url + a.get('href')

				categorie[categorie_name] = categorie_link

		del categorie['']

		return list(categorie.keys())


if __name__ == '__main__':
	print(get_categorie())
	