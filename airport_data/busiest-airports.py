'''
py -3 -m venv .venv
.venv\scripts\activate
'''

'''
https://www.freecodecamp.org/news/scraping-wikipedia-articles-with-python/
'''

# scraper ----- reads and makes class --> tree maker ---- makes an Element Tree --> xml-reader-writer
# three files: scraper, element tree maker, xml-reader-writer

import requests
from bs4 import BeautifulSoup

links = [ 
    # "https://en.wikipedia.org/wiki/Hartsfield%E2%80%93Jackson_Atlanta_International_Airport",
    # "https://en.wikipedia.org/wiki/Los_Angeles",
    # "https://en.wikipedia.org/wiki/Aktau_Airport",
    "https://en.wikipedia.org/wiki/List_of_airports_in_Turkey",
] 

def get_city_pop(cityurl : str): 
    # cityresponse = requests.get(url=cityurl)
    # citysoup = BeautifulSoup(cityresponse.content, 'html.parser')
    # content = citysoup.find(id="mw-content-text").div
    # table = content.find_all('table')[0].tbody.find_all('tr')
    pass


for l in links: 
    
    response = requests.get(
        url=l,
    )

    soup = BeautifulSoup(response.content, 'html.parser')

    title = soup.find(id="firstHeading")

    content = soup.find(id="mw-content-text").div
    table = content.find_all('table')[1].tbody.find_all('tr')

    for tr in table:
        if tr and tr.td and tr.td.a: 
            print(tr.td.a.string)
            cityurl = tr.td.a['href'] 
            get_city_pop(cityurl)
            
            if tr.find_all('td')[3].b:
                print(tr.find_all('td')[3].b.a.get_text())
            elif tr.find_all('td')[3].a: 
                print(tr.find_all('td')[3].a.get_text())
            
        if tr and tr.th and tr.th.get_text().find("Military airports") != -1:
            break
    # print(table)
