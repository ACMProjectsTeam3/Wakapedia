# Wakapedia
A MC Wikipedia.

## Files
* HTMLscraper.py: Main file; scrapes a given Bundle containing a url
* RandomCategoryScraper.py: Takes a Bundle (after it's run through HTMLscraper.py), randomly selects a category and scrapes the pages in that category
* CategoryScraper.py: Scrapes EVERY page in EVERY category in a Bundle (after it's run through HTMLscraper.py)
* ThreadedCategoryScraper.py: Does what CategoryScraper.py does, except threaded for efficiency/concurrency

Note: CategoryScraper.py and ThreadedCategoryScraper.py are unused because I did unnecessary work. We didn't need something this encompassing lol.
