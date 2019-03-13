from pymongo import MongoClient
import mongomock
# import urllibrequest

# client = MongoClient('mongodb://root:cdfa907be86f74b3e4358565ca@178.128.34.111:27017')
texts = MongoClient('mongodb://178.128.34.111:27017').db.texts
# for db in client.list_database_names():
#     print(db)

import os
import json

# texts = mongomock.MongoClient().db.texts

with open(os.path.join(os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))), 'sample_text.json'), 'rb') as fp:
    data = json.load(fp)
    texts.insert_one(data)

for text in texts.find({}):
    # print(text['caption'])
    for sentence in text['sentences']:
        number = sentence.get('number', None)
        translation = sentence.get('translation', None)
        if translation is not None and number is not None:
            # response = json.loads(
            #     urllib.request.urlopen(
            #         urllib.request.Request('https://qemotion.p.rapidapi.com/v1/emotional_analysis/get_emotions', headers={
            #             "X-RapidAPI-Key": "4b77b0bfc8msha1e193906f5df01p149009jsn4171810ad2fd",
            #             "Content-Type": "application/json; charset=UTF-8",
            #             "Authorization": "Token token=\"bc55ca0a8f5c8c41556f499a93f7077a\"",
            #             "lang": "en",
            #             "text": translation  
            #         })
            #     ).read().decode('utf-8')
            # )
            # emotions = response['content']['emotions']

            emotions = {
                'surprise': number,
                'calm': number,
                'fear': number,
                'sadness': number,
                'anger': number,
                'disgust': number
            }

            sentence['emotions'] = {
                'surprise': emotions['surprise'],
                'calm': emotions['calm'],
                'fear': emotions['fear'],
                'sadness': emotions['sadness'],
                'anger': emotions['anger'],
                'disgust': emotions['disgust']
            }
            texts.update_one({
                '_id': text['_id'], 
                'sentences' : {
                    '$elemMatch' : {
                        'number' : number
                    }
                }
            }, {
                '$set': {
                    'sentences.$.emotions' : {
                        'surprise': emotions['surprise'],
                        'calm': emotions['calm'],
                        'fear': emotions['fear'],
                        'sadness': emotions['sadness'],
                        'anger': emotions['anger'],                          
                        'disgust': emotions['disgust']
                    }
                }
            })
    
for text in texts.find({}):
    for sentence in text['sentences']:
        print(sentence)

