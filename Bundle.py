"""
This is the object that we pass to each component (the scraper, MC engine,
reconstructor, etc). Modify what your component needs to change, then
pass it down the line. Imagine an assembly line.
"""
class Bundle(object):
    __slots__ = ['text', 'paragraphs', 'URL', 'html', 'categories']
            # instantiate with URL of Wikipedia page
            # ctg is a flag, if it's true then categories should be retrieved
    def __init__(self, link, ctg):
                # This is a single string containing all the texts from the paragraphs.
                # Basically Bundle.paragraphs, but all in one string instead of a dictionary.
        self.text = ''
		# This is a dictionary of strings, where each string is the contents of
		# a paragraph and its key is the token where it should be in the HTML.
        self.paragraphs = {}
		# This is the URL of the page we need to get. It's a string.
        self.URL = link
		# This contains the HTML that we're modifying.
        self.html = ''
                # This is a list of all the categories that the Wikipedia article
                # belongs to.
        self.categories = ctg
