from typing import List 
import xml.etree.ElementTree as et 

def build_element(elementname, elementvalue) -> et.Element:
    ele = et.Element(elementname, {})
    ele.text = elementvalue
    return ele


    

class SeatingClass:
    class_name : str
    number : int

    def __init__(self, class_name, number):
        self.class_name = class_name
        self.number = number
        
    def toxml(self) -> et.Element:
        parent = et.Element("SeatingClass")
        parent.attrib['ClassName'] = self.class_name
        parent.attrib['Number'] = str(self.number)
        # parent.append(build_element("ClassName", self.class_name))
        # parent.append(build_element("Number", str(self.number)))
        return parent  

class Configuration: 
    classes : List[SeatingClass]

    def __init__(self):
        self.classes = []

    def toxml(self) -> et.Element:
        parent = et.Element("SeatingConfiguration")
        for c in self.classes:
            parent.append(c.toxml())
        return parent

class Airplane:
    aircraft_model : str
    number_in_fleet : int
    orders : int 
    passengers : List[Configuration]  
    notes : str 

    def __init__(self, aircraft_model, number_in_fleet, orders, notes):
        self.aircraft_model = aircraft_model
        self.number_in_fleet = number_in_fleet
        self.orders = orders 
        self.notes = notes 
        self.passengers = []

    def toxml(self) -> et.Element:
        parent = et.Element("AircraftModel")
        parent.append(build_element("ModelName", self.aircraft_model))
        parent.append(build_element("NumberInFleet", str(self.number_in_fleet)))
        parent.append(build_element("Orders", str(self.orders)))
        parent.append(build_element("Notes", self.notes))
        conf = et.Element('Configurations')
        for c in self.passengers:
            conf.append(c.toxml())
        parent.append(conf)
        return parent 

class Fleet:
    aircraft_types : List[Airplane]
    total_orders : int 
    total_inservice : int 

    def __init__(self, total_inservice, total_orders):
        self.total_inservice = total_inservice
        self.total_orders = total_orders
        self.aircraft_types = []

    def toxml(self) -> et.Element:
        pass 

