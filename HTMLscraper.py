"""
This gets the texts in paragraphs of a webpage given a URL
Returns Bundle object after updating text and HTML fields
"""

from bs4 import BeautifulSoup
from Bundle import Site, Bundle
import urllib

  ### bun:Bundle object from Bundle.py
def cleanhtml(bun):
    ### opens url so it's like a file
  link = urllib.urlopen(bun.URL)
    ### instantiate BeautifulSoup object
  soup = BeautifulSoup(link, 'lxml')
    ### dictionary of paragraphs
  doc = {}
    ### add token and count to replace paragraphs in HTML
  token = 'Waka'
  count = 0

    ### iterate thru the <p> tags
  for para in soup.find_all('p'):
      ### put raw text in dictionary
    doc[token+str(count)] = para.get_text()
      ### replace <p> contents with a token
    para.string = token + str(count)
      ### increment the token
    count+=1                          

    ### update Bundle with raw text
  bun.text = doc
    ### update Bundle with tokened html
  bun.site.html = str(soup)
  return bun
