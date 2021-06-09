import requests
from time import sleep
from bs4 import BeautifulSoup

def get (url, kwargs = {}):
    headers =  {
        'User-agent' : 'Mozilla/5.0' 
    }  
    requete = requests.get(url,params=kwargs,headers=headers) 
    print ('Response['+str(requete.status_code)+']')  
    return requete
 

class ipc () :
    def __init__(self):
        self.url = "https://www.ipc-computer.fr/pieces-detachees/alimentatione"

    def getAllArticles (self, url) :
        linksArticles = []
        page = get(url) 
        soup = BeautifulSoup(page.text, 'html.parser')
        nb_articles = int((((soup.find("div" ,{"class" : "sq_paginator clearfix"})).find("p")).findAll("b"))[2].get_text())
        page = int((((soup.find("div" ,{"class" : "sq_paginator clearfix"})).find("p")).findAll("b"))[1].get_text())
        params = {
            "page":0,
        }
        nb_page = int(nb_articles/page)
        
        for i  in range (1,nb_page):
            params["page"]=i
            page = get(url,params )       
            soup = BeautifulSoup(page.text, 'html.parser')
            divs = soup.select('tr[class*="productListing"]')
            for div in divs :
                try :
                    link = div.find("a" ,{"class" : "title"})
                    linksArticles.append(link)
                    #Funciton insert link in DB
                except :
                    print(i)
                    break
            sleep(2)
        return len(linksArticles)
ipc = ipc()

ipc.getAllArticles ( "https://www.ipc-computer.fr/pieces-detachees/alimentatione")
