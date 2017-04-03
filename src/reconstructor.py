from .Bundle import Bundle

def reconstruct(b):
    for key in b.paragraphs.keys():
        para = b.paragraphs[key]
        start = b.html.find(key)
        b.html = b.html[0:start] + para + b.html[start + len(key) : -1]
    return b
