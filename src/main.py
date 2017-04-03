from .Bundle import Bundle
from .HTMLscraper import scrape
from .reconstructor import reconstruct
from .MarkovChainer import CreateSentences
import sys

def run(article):
  bun = Bundle('https://en.wikipedia.org/wiki/' + str(article), True)
  bun = scrape(bun)
  bun = CreateSentences(bun)
  bun = reconstruct(bun)

  f = open(str(article) + '.html', 'w')
  f.write(bun.html)
  print ('done')
  return bun.html

if __name__ == "__main__":
    run(sys.argv[1])
