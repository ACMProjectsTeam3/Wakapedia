from Bundle import Bundle
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

    print (len(wikilinks))

      ### sends off the links in the list to be scraped to get the text from their page.
      ### Puts it all in one string.
    count = 1
    for page in wikilinks:
        tempbun = scrape(Bundle(page, False))
        print (count)
        count+=1
        ALL_TEXT += tempbun.text.translate(non_bmp_map)
        
    return ALL_TEXT

"""
This gets links to wikipedia pages from a category page.
Returns a list.
"""
def scrape_category_page(url):
    links = []
    soup = BeautifulSoup(urllib.request.urlopen(url), 'lxml')

      ### accounts for categories with over 200 pages
    link = soup.find('a', href=True, text='next page')
    if (link != None):
        links += scrape_category_page('https://en.wikipedia.org' + link['href'])

      ### sends links of wikipedia articles in the category to be scraped
    pages_in_category = soup.find('div', {'id':'mw-pages'}).find('div',{'class':'mw-category'})
    for obj in pages_in_category.findAll('a'):
        links.append('https://en.wikipedia.org' + obj['href'])
    return links

