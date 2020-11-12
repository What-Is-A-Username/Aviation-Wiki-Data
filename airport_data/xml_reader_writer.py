import xml.etree.ElementTree as ETree 
from bs4 import BeautifulSoup as BSoup
from xml.dom import minidom
from datastructures import Region, Airport, Runway

def read_xml(fileNameWithoutExtension : str):
    data = ETree.parse(fileNameWithoutExtension + ".xml")
    for child in data.getroot():
        print(child.tag, child.attrib)
        if child.tag == "RegionName":
            print(child.text)
    return data 

def write_xml(data : ETree.ElementTree, fileNameWithoutExtension : str, newlchr : str, indentchr : str):
    print('file location', __file__)
    xmlstr = minidom.parseString(ETree.tostring(data.getroot())).toprettyxml(newl=newlchr, indent=indentchr)
    with open(fileNameWithoutExtension + ".xml", "w", encoding='UTF-8') as f:
        f.write(xmlstr)

def get_string(data : ETree.ElementTree):
    return ETree.tostring(data.getroot(), encoding='UTF-8')

tree = read_xml("Cities")
element = ETree.Element("Something", { })
element.text = "something"
tree.getroot().append(element)
write_xml(tree, "output", '', '')

# Debug testing stuff for making new regions and airports
testregion = Region("Some new region", [
    Airport("xml", "name", "city", "coun", "reg", "lev", "icao", "iata", 8000, 1, 2, 3, 4, 5, 6, [Runway(3, "Grass")]),
    Airport("xml2", "name2", "city", "coun", "reg", "lev", "icao", "iata", 8000, 1, 2, 3, 4, 5, 6, [Runway(5, "Asphalt")])]
)
testtree = ETree.ElementTree(testregion.toxml())
write_xml(testtree, "testtree", '\n', '\t')
