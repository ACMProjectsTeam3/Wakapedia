from bs4 import BeautifulSoup
import re
import urllib

def cleanhtml(raw_html):
  soup = BeautifulSoup(raw_html, 'lxml')
  return soup.get_text()
