from requests_html import HTMLSession
from bs4 import BeautifulSoup
import pandas as pd
import argparse


searchterm ='ssd+1tb'

s = HTMLSession()
dealslist = []


url = f'https://www.amazon.com/s?k={searchterm}&page={1}&crid=1242MEW9WYNP&qid=1657136746&sprefix={searchterm}%2Caps%2C247&ref=sr_pg_{1}'

def getdata(url):
    r = s.get(url)
    r.html.render(sleep=2)
    soup = BeautifulSoup(r.html.html, 'html.parser')
    return soup  

def getdeals(soup):
    products = soup.find_all('div', {'data-component-type':'s-search-result'})
    
    for item in products:
        check = item.find_all('span', {'class': 'a-offscreen'})
        if check != []:
            title = item.find('a', {'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'}).text.strip()
            short_title = item.find('a', {'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'}).text.strip()[:25]
            link = item.find('a', {'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})['href']
            try:
                saleprice = float(item.find_all('span', {'class': 'a-offscreen'})[0].text.replace('$','').replace(',','').strip())
                oldprice = float(item.find_all('span', {'class': 'a-offscreen'})[1].text.replace('$','').replace(',','').strip())
            except:
                oldprice = float(item.find('span', {'class': 'a-offscreen'}).text.replace('$','').replace(',','').strip())
            try:
                reviews = float(item.find('span', {'class': 'a-size-base s-underline-text'}).text.strip())
            except:
                reviews = 0
    

        saleitem = {
            'title': title,
            'short_title': short_title,
            'link': link,
            'saleprice': saleprice,
            'oldprice': oldprice,
            'reviews': reviews            
            }
        dealslist.append(saleitem)
    return
 

for i in range(1,1000):        
    soup=getdata(f'https://www.amazon.com/s?k={searchterm}&page={i}&crid=1242MEW9WYNP&qid=1657136746&sprefix={searchterm}%2Caps%2C247&ref=sr_pg_{i}')
    print(f'Getting page: {i}')
    getdeals(soup)
    print(len(dealslist))
    if not soup.find('span',{'class':'s-pagination-item s-pagination-next s-pagination-disabled'}):
        pass
    else:
        break


df = pd.DataFrame(dealslist)
df['percentoff'] = 100 - ((df.saleprice / df.oldprice) * 100)
df = df.sort_values(by=['percentoff'], ascending=False)
df.to_csv(searchterm + '-bfdeals.csv', index=False)
print('Fin.')