from bs4 import BeautifulSoup

def cleanhtml(raw_html):
  soup = BeautifulSoup(raw_html, 'lxml')
  return soup.get_text()
