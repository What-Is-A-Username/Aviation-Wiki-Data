# scrapes data from wiki pages containing complete tables of airline's aircraft 
# either fetches new pages and saves them into the airline_fleet_html directory, or fetches from existing saves
# stores fleet data into .xml files in airline_fleet_data directory

from bs4 import BeautifulSoup
import xml.etree.ElementTree as et 
from xml.dom import minidom
from fleet_data_structures import Airplane, Fleet, Configuration, SeatingClass
from xml_reader_writer import write_xml
from wikipedia_package_test import make_html_file
import os

useSaved = 'y' in input('Use saved html? y = yes, n = no\n').lower()

if useSaved:
    file_name = input('Give the html file name, without directory location and without .html extension\n')
    file_os_path = os.getcwd() + '/airline_fleet_html/' + file_name + '.html'
else:
    wiki_title = input('Give the title of the wiki article\n')
    file_os_path = make_html_file(wiki_title)

index_of_column_header = int(input('Input the header\'s row index within the table: 0 = first, 1 = second\n'))


with open(file_os_path, encoding='utf-8') as f: 
    soup = BeautifulSoup(f, 'html.parser')

title = soup.find(id="firstHeading")

all_tables = soup.find_all('table')
table = None 
for t in all_tables:
    if t.caption and 'fleet' in str(t.caption).lower():
        table = t 
        break
    if t.tbody and t.tbody.tr and t.tbody.tr.th and 'fleet' in t.tbody.tr.th.text.lower():
        table = t
        break

if table != None:

    table_headers = [th.text.strip() for th in table.tbody.find_all('tr')[index_of_column_header].find_all('th')]
    print('found the headers of table', table_headers)

    table_full = table.tbody.find_all('tr')

    # get the passenger classes given
    passenger_key = [] 
    if table_full[index_of_column_header+1].td and table_full[index_of_column_header+1].td.a:
        passenger_key = 'Unassigned' 
        passenger_classes = ['Unassigned']
        table_entries = table_full[1:-1]
    else:
        passenger_key = table_full[index_of_column_header+1].find_all('th')
        passenger_classes = [ key.abbr['title'] for key in passenger_key if key.abbr and key.abbr.has_attr('title')]
        table_entries = table_full[2:-1]
    print('found the classes', passenger_classes)

    # loop through entries
    table_footer = table_full[-1]

    # current box to fill 
    row_index = 0
    col_index = 0 
    
    # current data
    data_table = [] 
    aircraft_model = ""
    note = ""

    # result
    airplanes = [] 

    for entry in table_entries:

        # get all td's with numbers in row 
        number_entries = entry.find_all('td')

        if entry.td and not(entry.th) and entry.td and entry.td.a or \
            entry.th and entry.th.text and 'cargo' in entry.th.text.lower(): 

            # output the previous aircraft model's data
            if len(data_table) > 0:

                number_in_service = data_table[0][0]
                number_of_orders = data_table[0][1]

                for r in range(len(data_table)):
                    data_table[r] = data_table[r][2:-1]

                print('model:', aircraft_model, 'note:', note)
                for row in data_table: 
                    print('\t', row)

                a = Airplane(aircraft_model, number_in_service, number_of_orders, note)

                for config in data_table:
                    new_config = Configuration() 
                    new_config.classes = [SeatingClass(passenger_classes[i], config[i] ) for i in range(len(passenger_classes))] 
                    a.passengers.append(new_config)

                airplanes.append(a)

            if entry.th and entry.th.text and 'cargo' in entry.th.text.lower():
                break

            row_span = 1
            # entries may feature multiple seating configurations which together span >1 row
            if entry.td.has_attr('rowspan'): 
                row_span = int(entry.td['rowspan'])
                # print("found anomalous row height of span ", row_span)

            aircraft_model = ' '.join(entry.td.a.text.strip().replace('\n', ' ').replace('\t', ' ').split())

            # storage of all data (in service + orders + classes + total): 
            data_table = [["-1" for i in range(0, len(passenger_classes) + 3)] for j in range(0, row_span) ]
            row_index = 0
            col_index = 0 
            # exclude the first one which is the aircraft model and the last one which is the notes
            number_entries = number_entries[1:-1]

            #get notes
            note_cell = entry.find_all('td')[-1] 
            note = ' '.join(note_cell.text.replace('\n', ' ').replace('\t', ' ').strip().split())

            while '[' in note and ']' in note:
                left = note.find('[')
                right = note.find(']')
                note = note[:left] + note[right + 1:]

        
        for number in number_entries:
            # find next unfilled cell 
            while data_table[row_index][col_index] != "-1":
                col_index += 1
                if col_index >= len(data_table[row_index]):
                    row_index += 1 
                    col_index = 0 
                
            cell_data = number.text.strip().replace('\n', '').replace('\t', '')
            while '[' in cell_data and ']' in cell_data:
                left = cell_data.find('[')
                right = cell_data.find(']')
                cell_data = cell_data[:left] + cell_data[right + 1:]
            number_rowspan = 1
            if number.has_attr('rowspan'):
                number_rowspan = int(number['rowspan'])
            number_colspan = 1
            if number.has_attr('colspan'):
                number_colspan = int(number['colspan'])
                
            for r in range(row_index, row_index + number_rowspan):
                for c in range(col_index, col_index + number_colspan): 
                    try:
                        data_table[r][c] = int(cell_data)
                    except ValueError: 
                        data_table[r][c] = 0 
  
    table_footer_th = table_footer.find_all('th')

    # note: totals may include cargo and other aircraft that may have already been excluded
    total_service = table_footer_th[1].text.strip()
    total_orders = table_footer_th[2].text.strip()

    print("total: in service", total_service, "orders: ", total_orders)

    final_tree = et.ElementTree(et.Element("FleetData"))

    for i in airplanes:
        final_tree.getroot().append(i.toxml())
    # print(minidom.parseString(et.tostring(final_tree.getroot())).toprettyxml(newl='\n', indent='\t')) 

    airline_name = file_os_path[file_os_path.find('_html/') + 6:file_os_path.find('.html')]
    new_file_name = airline_name.title().replace('Fleet', '').replace(' ', '') + '_Data'
    write_xml(final_tree, new_file_name, '\n', '\t')
