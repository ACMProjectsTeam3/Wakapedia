from bs4 import BeautifulSoup
from Bundle import Site, Bundle
import urllib, re

"""
This gets the texts in paragraphs of a webpage given a Bundle object
Returns Bundle object after updating text and HTML fields
"""

  ### bun:Bundle object from Bundle.py
def scrape(bun):
    ### opens url so it's like a file
  link = urllib.request.urlopen(bun.URL)
  soup = BeautifulSoup(link, 'lxml')
    ### dictionary of paragraphs
  doc = {}
    ### add token and count to replace paragraphs in HTML
  token = 'Waka'
  count = 0

    ### all the paragraph texts in one string
  alltxt = ''
    ### iterate thru the <p> tags
  for para in soup.find_all('p'):
      ### put raw text in dictionary
    doc[token+str(count)] = para.get_text()
    alltxt = alltxt + para.get_text()
      ### replace <p> contents with a token
    para.string = token + str(count)
    count+=1
 
    ### get the list of categories
  cats = []
  for cat in soup.find('div', {'id': 'catlinks'}).find('ul').findAll('li'):
      cats.append('https://en.wikipedia.org' + cat.find('a')['href'])

    ### update stuff in Bundle
  bun.paragraphs = doc
  bun.text = alltxt
  bun.site.html = str(soup)
  bun.categories = cats
    ### retrieve CSS file(s) links
  bun.site.CSS = soup.find_all('link', rel='stylesheet')
    ### retrieve js file(s) links
  bun.site.js = soup.find_all('script', src=re.compile('.*'))
  return bun

"""
x = Bundle('', '', 'https://en.wikipedia.org/wiki/Alpaca', Site('','',''), [])
x = scrape(x)

print (x.categories)
"""

