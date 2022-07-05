import requests
from bs4 import BeautifulSoup
import pandas as pd

reviewlist=[]

def get_soup(url):
    r =requests.get('http://localhost:8050/render.html',params={'url':url,'wait':2})
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup
    
def get_review(soup):
    reviews =soup.find_all('div',{'data-hook':'review'})
    try:
        for item in reviews:
            review={
            'product':soup.title.text.replace("Amazon.com: Customer reviews:","").strip(),
            'title':item.find('a',{'data-hook':'review-title'}).text.strip(),
            'rating':float(item.find('i',{'data-hook':'review-star-rating'}).text.replace('out of 5 stars','').strip()),
            'body': item.find('span', {'data-hook': 'review-body'}).text.strip(),
            }
            reviewlist.append(review)
    except:
        pass
        
        
for i in range(1,1000):        
    soup=get_soup(f'https://www.amazon.com/SPIDERCASE-Designed-Yellowing-Protectors-Case-Clear/product-reviews/B09NB8DN3Y/ref=cm_cr_getr_d_paging_btm_prev_1?ie=UTF8&reviewerType=all_reviews&pageNumber={i}')
    print(f'Getting page: {i}')
    get_review(soup)
    print(len(reviewlist))
    if not soup.find('li',{'class':'a-disabled a-last'}):
        pass
    else:
        break

df= pd.DataFrame(reviewlist)
df.to_csv('review.csv')

