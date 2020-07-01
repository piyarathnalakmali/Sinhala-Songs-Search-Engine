from elasticsearch import Elasticsearch
es=Elasticsearch([{'host':'localhost','port':9200}])

boost_dict = {
    "title": 1,
    "artist": 1,
    "writer": 1,
    "music": 1,
    "genre": 1,
    "beat": 1,
    "lyrics": 1
}
artist_keywords = ['ගැයූ', 'ගායකයා', 'ගායනා', 'ගයන', 'කියූ', 'කියන']
writer_keywords = ['ලියූ', 'රචිත', 'රචනා', 'ලියන']
musician_keywords = ['සංගීතවත්']
beat_keywords = ["4/4", "3/4", "4/4", "2/4", "6/8"]
popularity_keywords = ['හොඳම', 'ජනප්‍රිය', 'ප්‍රචලිත', 'ප්‍රසිද්ධ']
genre_keywords = ["ක්ලැසික්", "වත්මන් ගීත", "පැරණි පොප්ස්", "චිත්‍රපට ගීත", "ගෝල්ඩන් ඕල්ඩීස්", "ගෝල්ඩන් පොප්", "නව පොප්", "යුගල", "කණ්ඩායම් ගීත", "කැලිප්සෝ"]
synonyms =  open("/media/laka/Lakmali/Aca Sem7/DM&IR/my_app/synonyms.txt", "r").read().split("\n")
synonyms_list = [i.split(",") for i in synonyms]
for sublist in synonyms_list:
    sublist = [i.strip() for i in sublist]

# Check for simiar words
def get_similar_words(query_words):
    similar_words = []
    for sublist in synonyms_list:
        is_synonym = [i for i in query_words if i in sublist]
        if len(is_synonym) > 0:
            for i in sublist:
                similar_words.append(i)
    return similar_words

def search(query):
    query_words = query.split()
    query_words = [i.strip() for i in query_words]
    fields = []
    filters = {}
    manual_sort = False
    size = 50

    # Boost artist
    artist_keys = [i for i in query_words if i in artist_keywords]
    if len(artist_keys) > 0:
        boost_dict['artist'] = boost_dict['artist'] + 4

    # Boost writer
    writer_keys = [i for i in query_words if i in writer_keywords]
    if len(writer_keys) > 0:
        boost_dict['writer'] = boost_dict['writer'] + 4

    # Boost music (composor)
    music_keys = [i for i in query_words if i in musician_keywords]
    if len(music_keys) > 0:
        boost_dict['music'] = boost_dict['music'] + 4

    # Check for popularity related keywords
    popularity_keys = [i for i in query_words if i in popularity_keywords]
    if len(popularity_keys) > 0:
        manual_sort = True

    # Boost yrics
    if len(query_words) > 8:
        boost_dict['lyrics'] = boost_dict['lyrics'] + 1

    # Boost genre
    gen_keywords = []
    for i in genre_keywords:
         if query.find(i) != -1:
             gen_keywords.append(i)
             filters['genre'] = i
    if len(gen_keywords) > 0:
        boost_dict['genre'] = boost_dict['genre'] + 2

    # Boost beat
    b_keywords = []
    for i in beat_keywords:
         if query.find(i) != -1:
             b_keywords.append(i)
             filters['beat'] = i
    if len(b_keywords) > 0:
        boost_dict['beat'] = boost_dict['beat'] + 2

    # Check for numeric tokens
    for i in query_words:
        if i.isdigit():
            size = int(i)

    # Extent the query string with synonyms
    similar_words = get_similar_words(query_words)
    print (similar_words)
    if len(similar_words) > 0:
        for i in similar_words:
            query += ' '
            query += i

    for key in boost_dict.keys():
        field = key + '^' + str(boost_dict[key])
        fields.append(field)

    q = {
    "query": {
        "bool": {
            "must" : {
                "multi_match" : {
                    "query": query,
                    "fields": fields,
                    "fuzziness": "AUTO"
                }
            },
            "should": []
        }
    },
    "aggs": {
            "Genre Filter": {
                "terms": {
                    "field": "genre.keyword",
                    "size": 3
                }
            },
            "Artist Filter": {
                "terms": {
                    "field": "artist.keyword",
                    "size": 3
                }
            },
            "Lyrics Filter": {
                "terms": {
                    "field": "writer.keyword",
                    "size": 3
                }
            }
        }
    }
    q["size"] = size

    # Add filters for genre and beat
    for key, value in filters.items():
        q["query"]["bool"]["should"].append({"match": {key: value}})

    # Change sorting attribute to number of views
    if manual_sort:
        q["sort"] = {'views' : 'desc'}
    print (q)
    res = es.search(index='my-songs',body=q)
    return (res)
