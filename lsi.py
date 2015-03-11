from pyquery import PyQuery as pq
import nltk
import re
import sqlite3
import lxml
from simserver import SessionServer
import types

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

def readable_source(url):
    return str(url).split('.')[-1] != 'pdf'

if __name__ == "__main__":

    swfile = open("/usr/share/dict/stopwords")
    stopwords = swfile.readlines()
    stopwords = [ word.strip() for word in stopwords ]
    swfile.close()

    conn = sqlite3.connect("/Users/ryanmuller/workspace/pkb/data/pkb.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("select sources.url, content_html from sources join source_metadata on source_metadata.url = sources.url where sources.url not like '%.pdf' and content_html != '' order by sources.url")
    sources = cursor.fetchall()

    training_corpus = [ { 'id': str(source['url']), 'tokens': html_document_to_tokens(source['content_html'], stopwords) } for source in sources ]
    training_corpus = [ item for item in training_corpus if len(item['tokens']) > 0 ]

    service = SessionServer('/tmp/my_server') # resume server (or create a new one)
    service.train(training_corpus, method='lsi') # create a semantic model
    service.index(training_corpus)
