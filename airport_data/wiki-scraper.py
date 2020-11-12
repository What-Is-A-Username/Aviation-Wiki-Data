'''
py -3 -m venv .venv
.venv\scripts\activate
'''


import requests
from bs4 import BeautifulSoup

links = [ 
    "https://en.wikipedia.org/wiki/Hartsfield%E2%80%93Jackson_Atlanta_International_Airport"
    "https://en.wikipedia.org/wiki/Los_Angeles"
] 

for l in links: 
    response = requests.get(
        url=l,
    )
    soup = BeautifulSoup(response.content, 'html.parser')

    title = soup.find(id="firstHeading")

    content = soup.find(id="mw-content-text")
    table = content.table.tbody.find_all('tr')
    for tr in table:
        if tr.th and tr.th.string == " • Total":
            print(title.string, " population ", tr.td.a.string)

    # print(table)
