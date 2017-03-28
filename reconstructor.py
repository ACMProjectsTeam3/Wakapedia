import Bundle

object = Bundle()

def reconstruct(b):
    for key in b.paragraphs.keys():
        para = b.paragraphs[key]
        start = b.html.find[key]
        b.html = object.html[0:start] + para + object.html[start + len(key) : -1]
    return object
