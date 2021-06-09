import requests
from bs4 import BeautifulSoup


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

	return categorie


if __name__ == '__main__':
	print(len(get_categorie()))