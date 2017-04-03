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

  filename = 'html/' + str(article) + '.html'
  os.makedirs(os.path.dirname(filename), exist_ok=True)
  with open(filename, 'w') as f:
     f.write(bun.html)
  
  return bun.html

if __name__ == "__main__":
    run(sys.argv[1])
