import csv
import xml.etree.ElementTree as ETree 
from bs4 import BeautifulSoup as BSoup
from xml.dom import minidom
from datastructures import Region, Airport, Runway
from xml_reader_writer import write_xml

l = [ [3, 4], [1, 2], [5, 6]]
d = { x[0] : x[1] for x in l }

with open('countries.csv', newline='', encoding='utf-8') as csvfile:
    countryreader = csv.reader(csvfile, delimiter=',', lineterminator='\r\n')
    countryreader_list = list(countryreader)
    countryreader_list.pop(0)
    # store country by code : country name
    country_directory = { x[1] : x[2] for x in countryreader_list }

with open('runways.csv', newline='', encoding='utf-8') as csvfile:
    runwayreader = csv.reader(csvfile, delimiter=',', lineterminator='\r\n')
    runway_list = list(runwayreader)
    runway_list.pop(0)

    # store runways by airport ref number : list of runways
    runway_dict = { }
    for r in runway_list:
        if r[1] not in runway_dict:
            runway_dict[r[1]] = []
        length = 0 
        if r[3] == '':
            length = 0
        else:
            length = int(r[3])
        runway_dict[r[1]].append(Runway(str(round(float(length) / 3.280839895)), r[5]))


with open('airports.csv', newline='', encoding='utf-8') as csvfile:
    airportreader = csv.reader(csvfile, delimiter=',', lineterminator='\r\n')

    airportlist = list(airportreader)
    
    # include large airports with airline service only
    scheduled_service = [l for l in airportlist if l[11] == 'yes' if (l[2] == 'large_airport' or l[2] == 'medium_airport') and l[13] != '' ]

    # print(len(scheduled_service))
    # for l in scheduled_service: 
    #     print(l[3], l[10], country_directory[l[8]])

    """
    0       1       2      3        4               5              6            7
    "id","ident","type","name","latitude_deg","longitude_deg","elevation_ft","continent",
        8           9               10              11              12          
    "iso_country","iso_region","municipality","scheduled_service","iata_code",
        13          14          15              16
    "local_code","home_link","wikipedia_link","keywords"
    0       1        2                       3              4           5   6      7
    2434,"EGLL","large_airport","London Heathrow Airport",51.4706,-0.461941,83,"EU",
      8      9      10      11     12     13  14    15                                  16
    "GB","GB-ENG","London","yes","EGLL","LHR",,"http://www.heathrowairport.com/","https://en.wikipedia.org/wiki/Heathrow_Airport","LON, Londres"


    """

runway_types_found = [] 
country_codes_to_output = []

for code, country in country_directory.items(): 
    airports = [x for x in scheduled_service if x[8] == code]
    region = Region(country, []) 
    for x in airports:
        runways = []
        if x[0] in runway_dict:
            runways = runway_dict[x[0]]
            for r in runways:
                if r.SurfaceType not in runway_types_found:
                    runway_types_found.append(r.SurfaceType)
        region.Airports.append(Airport(x[0], x[3], x[10], country, country, 1, x[12], x[13], 0, 1, 1, 1, 1, 1, 1, runways))
    regionxml = region.toxml()
    tree = ETree.ElementTree(regionxml)
    #if code in country_codes_to_output:
    write_xml(tree, country, '\n', '\t')
    
print('runway types found ', runway_types_found)
    
    



    