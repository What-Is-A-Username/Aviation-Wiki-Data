import wikipedia
import os 

def make_html_file(wiki_title) -> str:
    current_os_path = os.getcwd()
    file_name = wiki_title + '.html'
    file_os_path = current_os_path + '/hubs_scripts/' + file_name

    page = wikipedia.page(wiki_title)
    page_html = page.html()

    with open(file_os_path, 'w', encoding='utf-8') as f:
        f.write(page_html)

    print('loaded wiki page of title', wiki_title, 'into html file of path', file_os_path)

    return file_os_path

if __name__ == '__main__':
    wiki_title = "filler"
    while len(wiki_title) > 0:
        wiki_title = input("Enter title of wiki article to load. Enter no characters to exit.")
        if len(wiki_title) == 0: 
            break
        make_html_file(wiki_title)
    print('Successfully exited.')

