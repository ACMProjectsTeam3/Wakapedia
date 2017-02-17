from Bundle import Site, Bundle
from bs4 import BeautifulSoup
from HTMLscraper import scrape
import urllib, sys

"""
This gets the text from all of the wikipedia pages
of all of the categories in the bundle. Returns a string.
"""

def scrape_category(bun):
      ### maps chars that the python terminal doesn't like to chars it does like
    non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
    ALL_TEXT = ''

      ### puts all of the wikipedia article links into one list
    wikilinks = []
    for link in bun.categories:
        wikilinks += scrape_category_page(link)
    #print (len(wikilinks))

      ### sends off the links in the list to be scraped to get the text from their page.
      ### Puts it all in one string.
    #count = 1
    for page in wikilinks:
        tempbun = scrape(Bundle('', '', page, Site('', '', ''), []))
        #print (count)
        #count+=1
        ALL_TEXT += tempbun.text.translate(non_bmp_map)
        
    return ALL_TEXT

"""
This gets links to wikipedia pages from a category page.
Returns a list.
"""
def scrape_category_page(url):
    links = []
    soup = BeautifulSoup(urllib.request.urlopen(url), 'lxml')
      ### lambda function that will get tags with class 'mw-category' and not include 'mw-category-group'
    divtag = soup.findAll(lambda tag: tag.name == 'div' and tag.get('class') == ['mw-category'])
    if len(divtag) == 0:
        return []
    for obj in divtag[len(divtag)-1].findAll('a'):
        links.append('https://en.wikipedia.org' + obj['href'])
    return links

