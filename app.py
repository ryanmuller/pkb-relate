import bottle
from bottle import route, static_file, request
from sys import argv
import uuid
import lxml
from pyquery import PyQuery as pq
import nltk
import re
import Pyro4

def html_document_to_tokens(doc, stopwords):
    try:
        pqdoc = pq(doc)
        doc = pqdoc.text()
    except lxml.etree.XMLSyntaxError:
        doc = re.sub(r'<\/?[^>]*>', '', doc) # remove html tags manually
    doc = doc.lower()
    doc = re.sub('https?:\/\/\S*', '', doc) # stray links
    doc = re.sub(r'[^a-z0-9-\s]', '', doc)
    doc = re.sub(r'\b[0-9-]+\b', '', doc)
    tokens = nltk.word_tokenize(doc)
    tokens = [ token for token in tokens if token not in stopwords]
    return tokens

@route('/')
def root():
        return static_file("app.html", root="./static/")

@route('/assets/<filepath:path>')
def asset(filepath):
        return static_file(filepath, root="./static/")

@route('/related', method='POST')
def related():
    swfile = open("/usr/share/dict/stopwords")
    stopwords = swfile.readlines()
    stopwords = [ word.strip() for word in stopwords ]
    swfile.close()

    doc = { 'tokens': html_document_to_tokens(request.forms.get('content'), stopwords) }
    service = Pyro4.Proxy(Pyro4.locateNS().lookup('gensim.testserver'))
    similar = service.find_similar(doc, max_results=5)
    return { 'related_urls': [ s[0] for s in similar ] }

bottle.run(host='0.0.0.0', port=argv[1])
