from bs4 import BeautifulSoup, SoupStrainer
from Bundle import Bundle
import urllib, re, time

"""
This gets the texts in paragraphs of a webpage given a Bundle object
Returns Bundle object after updating text and HTML fields
"""

  ### bun:Bundle object from Bundle.py
def scrape(bun):
    ### opens url so it's like a file
  link = urllib.request.urlopen(bun.URL)

  soup = None
    ### flag for retrieving categories (or not)
  if bun.categories:
    soup = BeautifulSoup(link.read().decode('utf-8'), 'lxml')
  else:
    p_tags = SoupStrainer('p')
    soup = BeautifulSoup(link.read().decode('utf-8'), 'lxml', parse_only=p_tags)

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
    alltxt = alltxt + para.get_text() + ' '
      ### replace <p> contents with a token
    para.string = token + str(count)
    count+=1

    ### get the list of categories
  cats = []
  if bun.categories:
    for cat in soup.find('div', {'id': 'catlinks'}).find('ul').findAll('li'):
      cats.append('https://en.wikipedia.org' + cat.find('a')['href'])

  for css in soup.find_all('link', rel='stylesheet'):
    css['href'] = '//en.wikipedia.org/' + css['href']

  for js in soup.find_all('script', src=re.compile('.*')):
    js['src'] = '//en.wikipedia.org/' + js['src']

    ### update stuff in Bundle
  bun.paragraphs = doc
  bun.text = alltxt
  bun.html = str(soup.encode('ascii', 'xmlcharrefreplace').decode('utf-8'))
  bun.categories = cats

  return bun

"""
x = Bundle('https://en.wikipedia.org/wiki/Alpaca', True)
x = scrape(x)

print (x.text)
"""
