import xml.etree.ElementTree as ETree 
from bs4 import BeautifulSoup as BSoup
from xml.dom import minidom
import os

def read_xml(fileNameWithoutExtension : str):
    data = ETree.parse(fileNameWithoutExtension + ".xml")
    for child in data.getroot():
        print(child.tag, child.attrib)
        if child.tag == "RegionName":
            print(child.text)
    return data 

def write_xml(data : ETree.ElementTree, fileNameWithoutExtension : str, newlchr : str, indentchr : str):
    current_os_path = os.getcwd()
    file_name = fileNameWithoutExtension + ".xml"
    file_os_path = current_os_path + '/hubs_xml/' + file_name
    xmlstr = minidom.parseString(ETree.tostring(data.getroot())).toprettyxml(newl=newlchr, indent=indentchr)
    with open(file_os_path, "w", encoding='UTF-8') as f:
        print('writing to file', file_os_path)
        f.write(xmlstr)

def get_string(data : ETree.ElementTree):
    return ETree.tostring(data.getroot(), encoding='UTF-8')


