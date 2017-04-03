from Bundle import Bundle
from HTMLscraper import scrape
from RandomCategoryScraper import scrape_category
from reconstructor import reconstruct
from MarkovChainer import CreateSentences
import sys

def main(article):
  bun = Bundle('https://en.wikipedia.org/wiki/' + str(article), True)
  bun = scrape(bun)
  bun = CreateSentences(bun)
  bun = reconstruct(bun)

  f = open(str(article) + '.html', 'w')
  f.write(bun.html)
  print ('done')
  return bun.html

if __name__ == "__main__":
    main(sys.argv[1])