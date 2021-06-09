import requests, time
from bs4 import BeautifulSoup

import mysql.connector

Database = {
	'host' : '127.0.0.1',
	'database' : 'ipc',
	'user' : 'arleme',
	'password' : '__@arleme'
}

class IPC():

	def __init__(self):
		self.arleme = ''
		self.db = mysql.connector.connect(**Database)
		self.cursor = self.db.cursor()


	def get(self, url, kwargs = {}):
		headers =  {
			'User-agent' : 'Mozilla/5.0' 
		}  
		requete = requests.get(url,params=kwargs,headers=headers) 
		print ('Response['+str(requete.status_code)+']')

		return requete

	def insert_article(self, categorie, url):
		query = '''
			INSERT IGNORE INTO 
				produits(url, categorie)
			VALUES
				(%s, %s)
		'''

		self.cursor.execute(query, (url, categorie))

		print(query)
		
		self.db.commit()

		time.sleep(1)


	# def update_article(self):
	# 	query = '''
	# 		INSERT IGNORE INTO 
	# 			Produits(name, url, image, prix, categorie, marque, description)
	# 		VALUES
	# 			(%s, %s, %s, %s, %s, %s, %s, %s)

	# 	'''

	# 	self.cursor.execute(query, (name, url, image, prix, categorie, marque, description))


	def get_article_list(self, categorie, url_categorie):
		linksArticles = []
		page = self.get(url_categorie) 
		soup = BeautifulSoup(page.text, 'html.parser')

		nb_articles = int((((soup.find("div" ,{"class" : "sq_paginator clearfix"})).find("p")).findAll("b"))[2].get_text())
		page = int((((soup.find("div" ,{"class" : "sq_paginator clearfix"})).find("p")).findAll("b"))[1].get_text())
		params = {
			"page":0,
		}
		nb_page = int(nb_articles/page)

		for i  in range (1,nb_page):
			params["page"]=i
			page = self.get(url_categorie,params )       
			soup = BeautifulSoup(page.text, 'html.parser')
			divs = soup.select('tr[class*="productListing"]')
			for div in divs :
				try :
					link = div.find("a" ,{"class" : "title"})
					linksArticles.append(link['href'])

					print(link['href'])
					self.insert_article(categorie, link['href'])

				except :
					print(i)
					break
			time.sleep(2)


		return linksArticles


	def get_categorie(self):
		url = 'https://www.ipc-computer.fr/'

		categorie = {}

		r = requests.get(url+'notebook-kategorien')

		src_code = BeautifulSoup(r.text, 'html.parser')

		for a in src_code.find_all('a'):
			link = a.get('href')
			if link.startswith('/pieces-detachees/'):
				categorie_name = a.get('title')
				categorie_link = url + a.get('href')

				categorie[categorie_name] = categorie_link

		return categorie


if __name__ == '__main__':

	scrapp = IPC()

	list_categorie = scrapp.get_categorie()

	print(list_categorie['Chargeurs'])

	print(scrapp.get_article_list('Chargeurs',list_categorie['Chargeurs']))
	