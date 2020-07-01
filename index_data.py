import json
from elasticsearch import Elasticsearch

es=Elasticsearch([{'host':'localhost','port':9200}])

f = open('./data/songs_corpus.json', encoding="utf8")
s = f.read()
data = json.loads(s.replace('\r\n', ''),strict=False)
count = 0
for i in range(len(data)):
    res=es.index(index='my-songs',doc_type='songs',id=i,body=data[i])
    count += 1
print (count)
