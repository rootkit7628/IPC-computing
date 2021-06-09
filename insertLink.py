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
    
     def getDetailsArticle(self, url) :
        article = {

        }
        page = get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        try :

            #nom de l'article
            article["name"] =  re.sub('\s+',' ',(str((soup.find("h1",{"class":"pageHeading"})).get_text())))

            #prix de l'article
            article["price"] = int(str((soup.find("span",{"itemprop":"price"})).get_text()).replace(".00",""))*4596
            
            #marque de l'articles 
            marques = [
                "Asus" , "Asus" , "Chicony" , "Clevo", "Dell" , "Delta electronics" ,"FSP", "Fujitsu", 
                "HP" , "Lenovo", "LiteOn","Medion" , "MSI" , "Panasonic" , "Samsung" ,"Sony" ,
                "Toshiba", "Treksor" , "Worthmann"
            ]
            for marque in marques :
                brand = ""
                a = article["name"].find(str(marque))
                if int(a) > -1 :
                    brand = marque
                    break
            
            article["brand"] = brand

            #Les liens de l'images :
            

            #La descriptions de 
            try :
                divs  = soup.find("div" ,{"id":"tabContent0"})
                divs = re.sub('\s+',' ',(divs.get_text()))
            except:
                divs = ""

            article["description"] = divs
        except :
            print("""
                    !!!!!!!!!!
                    FAIL
                    !!!!!!!!!!
            """)
        return article
ipc = ipc()

ipc.getAllArticles ( "https://www.ipc-computer.fr/pieces-detachees/alimentatione")
