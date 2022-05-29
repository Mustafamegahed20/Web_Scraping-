import requests 
import pandas as pd
from bs4 import BeautifulSoup


records=[]

page_num =0
while True:

    record = requests.get(f"https://wuzzuf.net/search/jobs/?a=hpb&q=python&start={page_num}")



    src =record.content 

    soup = BeautifulSoup(src,"lxml")


    page_limit = int(soup.find("strong").text)

    if(page_num > page_limit//15):
       print("page terminate")
       break
    job_titles = soup.find_all("h2",{"class":"css-m604qf"})
    company_names = soup.find_all("a",{"class":"css-17s97q8"})
    loacations = soup.find_all("span",{"class":"css-5wys0k"})
    job_types = soup.find_all("span",{"class":"css-1ve4b75 eoyjyou0"})


    for i in range(len(job_titles)):
        job_title=job_titles[i].a.text.strip()
        company_name=company_names[i].text.strip()
        loacation=loacations[i].text.strip()
        job_type=job_types[i].text.strip()
        records.append((job_title,company_name,loacation,job_type))

    page_num +=1
    






df = pd.DataFrame(records, columns=['job_titles', 'company_names', 'loacations', 'job_type'])  

with open("wuzzaf.csv","w") as f:
     df.to_csv(f) 


