import time
from bs4 import BeautifulSoup
import pandas as pd
import requests


r = requests.get('https://geographic.org/streetview/usa/index.html')
soup = BeautifulSoup(r.content,'html.parser')
table = soup.find('div',{'class':'listmain'}).find_all('a')

all_streets = []
for x in table:
    ln = x.get('href')
    lnnn = x.text
    for_all = ln.replace('/index.html','')
    print(for_all)
    r =requests.get(f'https://geographic.org/streetview/usa/{ln}')
    time.sleep(1)
    soup = BeautifulSoup(r.content,'html.parser')
    citys = soup.find('div',{'class':'listmain'}).find_all('a')
    for city in citys:
        d = city.text.lower()
        print(d)
        r = requests.get(f'https://geographic.org/streetview/usa/{for_all}/{d}/index.html')
        time.sleep(1)      
        try:
            soup = BeautifulSoup(r.content,'html.parser')
            sts = soup.find('div',{'class':'listmain'}).find_all('a') 
        except:
            pass    
        for s in sts:
            c = s.text.lower()
            try:
                c = c.split(' ')
                c = '_'.join(c)
                print(c)
            except:
                pass    
            
            r = requests.get(f'https://geographic.org/streetview/usa/{for_all}/{d}/{c}.html')
            time.sleep(1)

            try:
                soup = BeautifulSoup(r.content,'html.parser')
                adreeses = soup.find('div',{'class':'listmain'}).find_all('li')
            except:
                continue    
            
            for adress in adreeses:
                main = adress.text.replace('\xa0',',')
                print(f'Scraping Running For ---------{d} -------> {c}---> In--------> {lnnn}')

                data_dict = {
                    'State':lnnn,
                    'City_1':d,
                    'City_2':c,
                    'Streets':main
                }

                all_streets.append(data_dict)
    df = pd.DataFrame(all_streets)
    df.to_csv(f'{lnnn}_Of_Streets.csv') 
              





    
    # 
    
    