# Aviation-Wiki-Data

A collection of Python scripts used to extract airport and airline data from Wikipedia pages and .csv files. Scanning of HTML is done using tools from the [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/) library. Extracted data is outputted into XML files for downstream applications.

## Functionalities

### Global airport directory sorted by country/region/territory ([csv_airports.py](/airport_data/csv_airports.py))
Reads .csv files containing global airport information obtained from [OurAirports](https://ourairports.com/data/), and combines data into uniform data structures for output into .xml files organized by country/region/territory in the [airport_data](airport_data) folder.

### Country-specific airport data ([busiest-airports.py](airport_data/busiest-airports.py))
Reads Wikipedia pages that list airports in a particular country (example: [Airports in Turkey](https://en.wikipedia.org/wiki/List_of_airports_in_Turkey)) and extracts airport locations and names for printing to the console.

### Airlines sorted by airport hub ([hubs_reader.py](hubs_scripts/hubs_reader.py))
Extracts data about global hub airports, and their local airlines, from the .html file of the [Hub Airport Wikipedia page](https://en.wikipedia.org/wiki/List_of_hub_airports). This airline data is outputted into an [.xml file](hubs_xml/Airport_Hub_Data.xml).

### Airline fleet composition ([airline_fleet_reader.py](airline_fleet_data/airline_fleet_reader.py))
Scans the HTML of a specified Wikipedia page which contains a table listing the airline's entire fleet of aircraft (example: [Air France](https://en.wikipedia.org/wiki/Air_France_fleet)). For each fleet it identifies the aircraft model names, number and passenger seating configurations for output to .xml files organized by airline name in the [airline_fleet_xml](airline_fleet_xml) folder.

## Disclaimer
Use and run this code at your own risk. By cloning or downloading any portion of this repository, you agree that the [@What-Is-A-Username](https://github.com/What-Is-A-Username) will hold no liability for any harm done, including but not limited to computer damage or irreversible deletion of user files.


