import xml.etree.ElementTree as et 
from typing import List
 
def build_element(elementname, elementvalue) -> et.Element:
    ele = et.Element(elementname, {})
    ele.text = elementvalue
    return ele

class Runway:
    Length : int 
    SurfaceType : str

    def __init__(self, length : int, SurfaceType : str):
        self.Length = length
        self.SurfaceType = SurfaceType

    def toxml(self) -> et.Element: 
        parent = et.Element("Runway")
        parent.append(build_element("Length", str(self.Length)))
        parent.append(build_element("SurfaceType", self.SurfaceType))
        return parent 
    

class Airport:
    def __init__(self, UniqueXMLID, AirportName, CityName, CountryName, RegionName, AirportLevel, ICAO, IATA, Pop, Gates, Hangars, Buildings, BaseOrigin, WealthRating, BaseAppeal, Runways : List[Runway]):
        self.UniqueXMLID = UniqueXMLID
        self.AirportName = AirportName
        self.CityName = CityName
        self.CountryName = CountryName
        self.RegionName = RegionName
        self.AirportLevel = AirportLevel
        self.ICAO = ICAO
        self.IATA = IATA
        self.Pop = Pop
        self.Gates = Gates
        self.Hangars = Hangars
        self.Buildings = Buildings
        self.BaseOrigin = BaseOrigin
        self.WealthRating = WealthRating
        self.BaseAppeal = BaseAppeal
        self.Runways = Runways

    Runways : List[Runway]
    UniqueXMLID : str 
    AirportName : str
    CityName : str
    AirportLevel : int 
    CountryName : str
    RegionName : str
    ICAO : str
    IATA : str
    Pop : int
    Gates : int
    Hangars : int
    Buildings : int 
    BaseOrigin : int
    WealthRating : int

    def toxml(self) -> et.Element: 
        element = et.Element("Airport", {})
        element.append(build_element("UniqueXMLID", self.UniqueXMLID))
        element.append(build_element("AirportName", self.AirportName))
        element.append(build_element("AirportLevel", str(self.AirportLevel)))
        element.append(build_element("CityName", self.CityName))
        element.append(build_element("CountryName", self.CountryName))
        element.append(build_element("RegionName", self.RegionName))
        element.append(build_element("ICAOCode", self.ICAO))
        element.append(build_element("IATACode", self.IATA))
        element.append(build_element("Population", str(self.Pop)))
        element.append(build_element("GateNumbers", str(self.Gates)))
        element.append(build_element("HangarNumbers", str(self.Hangars)))
        element.append(build_element("BuildingNumbers", str(self.Buildings)))
        element.append(build_element("BaseOrigin", str(self.BaseOrigin)))
        element.append(build_element("WealthRating", str(self.WealthRating)))
        runways = et.Element("Runways") 
        for r in self.Runways:
            runways.append(r.toxml())
        element.append(runways)
        return element
        
class Region:
    Airports = []

    def __init__(self, regionName : str, airports : List[Airport] = []):
        self.RegionName = regionName 
        self.Airports = airports 

    def toxml(self) -> et.Element: 
        regionelement = et.Element("RegionData") 
        parent = et.Element("Airports")
        for airport in self.Airports:
            parent.append(airport.toxml())
        regionelement.append(parent)
        regionelement.append(build_element("RegionName", self.RegionName))
        return regionelement