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
    hotels = soup.find_all('div', {'class':'facility-detail js-facility-detail'})
    more_inf=soup.find_all('div',{'class':'facility-detail-modal js-facility-detail-modal oec-modal'})
            
    for i in range(len(hotels)):
         
        try:
            title = hotels[i].find('div', {'class': 'title'}).text.strip()
            category= hotels[i].find('div', {'class': 'category'}).text.strip()
            location=more_inf[i].find_all('div',{'class':'facility-detail-lead'})[1].text.replace("  ",'').strip()
            telephone=more_inf[i].find('a',{'class':'facility-detail-link facility-detail-phone'}).find('div',{'class':'info-wrapper'}).text.replace('Téléphone\n','').strip()
            website=more_inf[i].find('a',{'class':'facility-detail-link facility-detail-site'}).find('div',{'class':'info-wrapper'}).text.replace('Site internet\n','').strip()
            mail=more_inf[i].find('a',{'class':'facility-detail-link facility-detail-mail'}).find('div',{'class':'info-wrapper'}).text.replace('Adresse email\n','').strip()
        except:
            pass
        try:
            saleitem = {
                'title': title,
                'category': category,
                'location': location,
                'telephone': telephone,
                'website': website,
                'mail': mail            
                }
            dealslist.append(saleitem)
        except:
            pass
    return

for i in range(1,1258):        
    url=f'https://www.classement.atout-france.fr/recherche-etablissements?p_p_id=fr_atoutfrance_classementv2_portlet_facility_FacilitySearch&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&_fr_atoutfrance_classementv2_portlet_facility_FacilitySearch_performSearch=1&_fr_atoutfrance_classementv2_portlet_facility_FacilitySearch_page={i}&_fr_atoutfrance_classementv2_portlet_facility_FacilitySearch_is_luxury_hotel=no'
    soup=getdata(url)
    print(f'Getting page: {i}')
    getdeals(soup)
    print(len(dealslist))
    


df = pd.DataFrame(dealslist)

df.to_csv('-hotel.csv', index=False)
print('Fin.')