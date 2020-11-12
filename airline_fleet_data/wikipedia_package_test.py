import wikipedia
import os 

def make_html_file(wiki_title) -> str:
    current_os_path = os.getcwd()
    file_name = wiki_title + '.html'
    file_os_path = current_os_path + '/airline_fleet_html/' + file_name

    page = wikipedia.page(wiki_title)
    page_html = page.html()

    with open(file_os_path, 'w', encoding='utf-8') as f:
        f.write(page_html)

    return file_os_path