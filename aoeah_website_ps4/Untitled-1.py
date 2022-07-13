from requests_html import HTMLSession
from bs4 import BeautifulSoup
import pandas as pd
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import pandas as pd


s = HTMLSession()
dealslist = []



def getdata(url):
    r = s.get(url)
    r.html.render(sleep=1)
    soup = BeautifulSoup(r.html.html, 'html.parser')
    return soup  

def getdeals(soup):
    hotels = soup.find_all('div', {'class':'goldrl-box decals-style'})

    for i in range(len(hotels)):         
        try:
            title = hotels[i].find('div', {'class': 'rl-name'}).text.strip()
            img='https://www.aoeah.com/'+ str(hotels[i].find('div', {'class': 'rl-img'}).find('img')['src'].replace('https://www.aoeah.com/','').replace(' ',''))
            
            for x in range(0,11):
                price=hotels[i].find('div',{'class':'input-na items-color'}).find_all('li')[x].find('em').text.strip()
                color=hotels[i].find('div',{'class':'input-na items-color'}).find_all('li')[x].find('span').text.strip()

                saleitem = {
                'title': title,
                'img':img,      
                'color':price, 
                'price':color,

                }
                dealslist.append(saleitem)           
        except:
            pass



    return 

url='https://www.aoeah.com/rocket-league-items/ps4'
soup=getdata(url)
getdeals(soup)
print(len(dealslist))
    


df = pd.DataFrame(dealslist)

df.to_csv('-ps4.csv', index=False)
print('Fin.')