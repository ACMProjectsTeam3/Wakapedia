"""
This encapsulate all the components of a website.
"""
class Site(object):
    def __init__(self, html, CSS, js):
		
		# This is the html. It's a single string.
        self.html = html
		# The CSS is an array of strings that represent potentially
		# multiple css files.
        self.CSS = CSS
		# This is also a list of strings that represent potentially
		# multiple js files.
        self.js = js

"""
This is the object that we pass to each component (the scraper, MC engine,
reconstructor, etc). Modify what your component needs to change, then
pass it down the line. Imagine an assembly line.
"""
class Bundle(object):
    def __init__(self, txt, link, site):
		# This is a dictionary of strings, where each string is the contents of
		# a paragraph and its key is the token where it should be in the HTML.
        self.text = txt
		# This is the URL of the page we need to get. It's a string.
        self.URL = link
		# This is an instance of Site, and is what we need to send back to the
		# user. This contains the HTML that we're modifying.
        self.site = site

