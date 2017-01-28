class Site(object):
    def __init__(self, html, CSS, js):
        self.html = html
        self.CSS = CSS
        self.js = js

class Bundle(object):
    def __init__(self, txt, link, site):
        self.text = txt
        self.URL = link
        self.site = site

