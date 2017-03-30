from Bundle import Bundle
from bs4 import BeautifulSoup
from HTMLscraper import scrape
from random import randint
import urllib, sys

"""
This gets the text from all of the wikipedia pages
of a randomly selected category in the bundle. Returns a string.
"""

def scrape_category(bun):
      ### maps chars that the python terminal doesn't like to chars it does like
    non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
    ALL_TEXT = ''

      ### choose a random category from the list and get a list of its wikipedia articles
    wikilinks = []
    ran_cat = bun.categories[randint(0, len(bun.categories)-1)]
    print (ran_cat)
    scrape_category_page(ran_cat, wikilinks)
    
      ### sends off the links in the list to be scraped to get the text from their page.
      ### Puts it all in one string.
    count = 1
    for page in wikilinks:
        tempbun = scrape(Bundle(page, False))
        #print (count)
        count+=1
        ALL_TEXT += tempbun.text.translate(non_bmp_map)
        
    return ALL_TEXT

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
                #print (str(len(links)) + obj['href'])
            else:
                break

       ### accounts for categories with over 200 pages
    link = soup.find('a', href=True, text='next page')
    if (link != None and len(links) < 500):
        scrape_category_page('https://en.wikipedia.org' + link['href'], links)

