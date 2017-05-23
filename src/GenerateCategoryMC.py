from bs4 import BeautifulSoup, SoupStrainer
from .MarkovMaker import TrainAndSaveString
import urllib, os, sys

"""
This gets links to wikipedia pages from a category page.
Returns a list.
"""

def scrape_category_page(url, links):
    soup = BeautifulSoup(urllib.request.urlopen(url), 'lxml')

      ### sends links of wikipedia articles in the category to be scraped
    pages_in_category = soup.find('div', {'id':'mw-pages'}).find('div',{'class':'mw-category'})

    if (pages_in_category != None):
        for obj in pages_in_category.findAll('a'):
            if (len(links) < 500):
                links.append('https://en.wikipedia.org' + obj['href'])
                print (str(len(links)) + obj['href'])
            else:
                break

       ### accounts for categories with over 200 pages
    link = soup.find('a', href=True, text='next page')
    if (link != None and len(links) < 500):
        scrape_category_page('https://en.wikipedia.org' + link['href'], links)


"""
This gets the texts in the paragraphs of a webpage.
Returns a string
"""
def scrape(url):
      ### opens url so it's like a file
    try:
        link = urllib.request.urlopen(url)
    except urllib.error.HTTPError:
        return ''

    soup = BeautifulSoup(link.read().decode('utf-8'), 'lxml', parse_only=SoupStrainer('p'))

    alltxt = ''
      ### iterate thru the <p> tags
    for para in soup.find_all('p'):
        alltxt = alltxt + para.get_text() + ' '

    return alltxt

"""
Scripty script
"""

def generate_category_chains(article):
    CATEGORIES = set()
    while (len(CATEGORIES) < 1):
        #url = urllib.request.urlopen('https://en.wikipedia.org/wiki/Special:Random')
        url = urllib.request.urlopen('https://en.wikipedia.org/wiki/' + str(article))
        soup = BeautifulSoup(url, 'lxml')

        #print (soup.title.string)

            ### get categories in the random wiki page
        for cat in soup.find('div', {'id': 'catlinks'}).find('ul').findAll('li'):
    	   ### markov chain it if we haven't already
              if not os.path.isfile('./Categories/' + cat.string + '.mc'):
                 ### SWITCH IF STATEMENTS OF STATE SIZE IS CHANGED
              #if cat.string not in CATEGORIES:
                    cattext = ''
                    links = []
                    scrape_category_page('https://en.wikipedia.org' + cat.find('a')['href'], links)
                    for link in links:
                        cattext = cattext + "\n" + scrape(link)
                    print (cat.string)
                    if cattext != "":
                        TrainAndSaveString(cattext, './Categories/' + cat.string + '.mc')
		        #filename = './Categories/' + cat.string + '.txt'
		        #os.makedirs(os.path.dirname(filename), exist_ok=True)
		        #with open(filename, 'w') as file:
		        #    file.write(cattext)

                    CATEGORIES.add(cat.string)

    print (CATEGORIES)

if __name__ == "__main__":
    generate_category_chains(sys.argv[1])
