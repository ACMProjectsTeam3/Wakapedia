from Bundle import Bundle
from bs4 import BeautifulSoup, SoupStrainer
from HTMLscraper import scrape
import urllib, sys, threading

    ### Thread object needed to make threads with urls
class catThread(threading.Thread):
    def __init__(self, url):
        threading.Thread.__init__(self)
        self.url = url
    def run(self):
        scrape_category_page(self.url)

lock = threading.Lock()

"""
This gets the text from all of the wikipedia pages
of all of the categories in thedata between threads bundle. Returns a string.
"""
def scrape_category(bun):
    global ALL_TEXT, non_bmp_map, threads, count
    ALL_TEXT = ''
    count = 1
    
      ### maps chars that the python terminal doesn't like to chars it does like
    non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

      ### process each category in a new thread
    threads = []
    for link in bun.categories:
        try:
            t = catThread(link)
              ### kills the baby thread if momma thread dies
            t.daemon = True
            t.start()
            threads.append(t)
        except:
            print ("Error: Unable to thread.")
            
      ### wait for all the threads to finish so the main thread doesn't just nope out
    for thr in threads:
        thr.join()
    
    return ALL_TEXT

"""
This gets links to wikipedia pages from a category page.
Returns a list.
"""
def scrape_category_page(url):
    global ALL_TEXT, non_bmp_map, threads, count
    soup = BeautifulSoup(urllib.request.urlopen(url), 'lxml', parse_only=SoupStrainer('div'))

      ### accounts for categories with over 200 pages
    link = soup.find('a', href=True, text='next page')
    if (link != None):
        try:
            t = catThread('https://en.wikipedia.org' + link['href'])
            t.daemon = True
            t.start()
            threads.append(t)
        except:
            print ("Error: Unable to thread.")

      ### sends links of wikipedia articles in the category to be scraped
    pages_in_category = soup.find('div', {'id':'mw-pages'}).find('div',{'class':'mw-category'})
    for obj in pages_in_category.findAll('a'):
        tempbun = scrape(Bundle('https://en.wikipedia.org' + obj['href'], False))
        with lock:
            ALL_TEXT += tempbun.text.translate(non_bmp_map)
            print (count)
            count += 1    
