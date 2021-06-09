import requests, time, re
from bs4 import BeautifulSoup

import mysql.connector

Database = {
	'host' : '127.0.0.1',
	'database' : 'ipc',
	'user' : 'arleme',
	'password' : '******'
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

	def get_list_url(self):
		query = '''
			SELECT id, url 
			FROM produits WHERE name IS NULL
		'''

		self.cursor.execute(query)

		list_url = self.cursor.fetchall()

		return list_url

		time.sleep(1)


	def insert_article(self, categorie, url):
		query = '''
			INSERT IGNORE INTO 
				produits(url, categorie)
			VALUES
				(%s, %s)
		'''

		self.cursor.execute(query, (url, categorie))

		self.db.commit()

		print("article inserted")

		time.sleep(1)


	def update_article(self, name, image, prix, marque, description, id_article):
		query = '''
			UPDATE 
				produits
			SET
				name = %s, image = %s, prix = %s, marque = %s, description = %s
			WHERE
				id = %s
		'''

		self.cursor.execute(query, (name, image, prix, marque, description, id_article))

		self.db.commit()

		print("article updated")

		time.sleep(1)


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

		for i  in range (73,nb_page):
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


	def getDetailsArticle(self, url) :

		article = {}

		page = self.get(url)
		soup = BeautifulSoup(page.text, 'html.parser')
		try :

			marques = [
				"Asus" , "Asus" , "Chicony" , "Clevo", "Dell" , "Delta electronics" ,"FSP", "Fujitsu", 
				"HP" , "Lenovo", "LiteOn","Medion" , "MSI" , "Panasonic" , "Samsung" ,"Sony" ,
				"Toshiba", "Treksor" , "Worthmann"
			]

		    #nom de l'article

			try:
				article["name"] =  re.sub('\s+',' ',(str((soup.find("h1",{"class":"pageHeading"})).get_text())))
				article["prix"] = int(str((soup.find("span",{"itemprop":"price"})).get_text()).replace(".00",""))*4596
				image_list = " ; ".join(['https://www.ipc-computer.fr/'+img['src'] for img in soup.find_all('img',{'itemprop':'image'})])
			except:
				image_list = ""
			
			for marque in marques :
				brand = ""
				a = article["name"].find(str(marque))
				if int(a) > -1 :
					brand = marque
					break

			article["marque"] = brand
			article["image"] = image_list

			try :
				divs  = soup.find("div" ,{"id":"tabContent0"})
				divs = re.sub('\s+',' ',(divs.get_text()))
			except:
				divs = ""

			article["description"] = divs
		except  :
			print("""
				!!!!!!!!!!
				FAIL
				!!!!!!!!!!
			""")
		    
		return article


if __name__ == '__main__':

	# scrapp = IPC()

	# # list_categorie = scrapp.get_categorie()

	# # print(list_categorie['Chargeurs'])

	# # print(scrapp.get_article_list('Chargeurs',list_categorie['Chargeurs']))

	# articles = scrapp.get_list_url()

	# for article in articles:
	# 	print(article[1])
	# 	detail = scrapp.getDetailsArticle(article[1])
	# 	print(detail)
	# 	scrapp.update_article(detail['name'],detail['image'],detail['prix'],detail['marque'],detail['description'], article[0])
