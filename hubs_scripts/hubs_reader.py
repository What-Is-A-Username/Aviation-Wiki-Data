# scrapes data from the wiki page 'List of hub airports' from file

from bs4 import BeautifulSoup
import xml.etree.ElementTree as et 
from xml.dom import minidom
from xml_reader_writer import write_xml
from wikipedia_package_test import make_html_file
import os

file_os_path = os.getcwd() + '/hubs_scripts/List of hub airports.html'

with open(file_os_path, encoding='UTF-8') as f: 
    soup = BeautifulSoup(f, 'html.parser')

title = soup.find(id="firstHeading")

content = soup.div.contents

foundstart = False

# output data structure; organized by airport_name : [airline_name]
hubs = { }

for entry in content:
    if not foundstart:
        if entry.name != 'h2':
            continue 
        else:
            foundstart = True
    elif entry.name == 'ul':
        for i in entry.contents :
            if i.name == 'li':
                # hubs[i.a['title']] = [a.a['title'] for j in i.contents if j.name == 'ul' for a in j.find_all('li')]
                for j in i.contents:
                    if j.name == 'ul':
                        airlines = j.find_all('li')
                        hubs[i.a['title']] = [a.a['title'] for a in airlines]
                        break

# things to remove from airline name
artifacts = [' (airline)', ' (page does not exist)']
final_tree = et.ElementTree(et.Element('HubAirports'))

for key, value in hubs.items():
    hub = et.Element("Airport")
    hub_name = et.Element("AirportName")

    

    hub_name.text = key

    hub.append(hub_name)
    airline_parent = et.Element("LocalAirlines")
    for airline in value:
        air = et.Element("Airline")
        for a in artifacts:
            airline = airline.replace(a, '')
        air.text = airline
        airline_parent.append(air)
    hub.append(airline_parent)
    final_tree.getroot().append(hub)    

write_xml(final_tree, 'Airport_Hub_Data', '\n', '\t')