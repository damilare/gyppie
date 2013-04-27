from flask import Flask, jsonify, render_template
import json
import requests

app = Flask(__name__)
app.debug = True

@app.route('/photos/<woe_id>')
def get_photos_by_woeid(woe_id):
    payload = {}
    payload['woe_id'] = woe_id
    payload['api_key'] = '0879b2436186cf87de5a00611135d776'
    payload['format'] = 'json'
    payload['method'] = 'flickr.photos.search'
    
    flickr_photos = []
    fr_resp = requests.get('http://api.flickr.com/services/rest/', params=payload)

    if fr_resp.status_code == 200:
        fr_photo_set = json.loads(fr_resp.content[14:-1])
        photos = fr_photo_set['photos']['photo']

        for photo in photos:
            flickr_photos.append('http://farm9.staticflickr.com/{0}/{1}_{2}_z.jpg'.format(photo['server'], photo['id'], photo['secret']))
    
    return jsonify({'data': flickr_photos})

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()

# api_url = 'http://bbc.api.mashery.com/juicer-ld-api/articles.json'
# query_dict = {'binding': 'a',
#               'where': '?a cwork:tag ?thing . ?a <http://www.ontotext.com/owlim/lucene#articles> "crime OR murder" . <http://dbpedia.org/resource/London> geo-pos:lat ?lat . <http://dbpedia.org/resource/London> geo-pos:long ?long . ?thing omgeo:nearby(?lat ?long "25mi") .', 
#               'api_key': 'kzjvv89zfh43zjcz6gdhjcd3', 
#               'limit': '5'}

# if __name__ == '__main__':
#     response = requests.get(api_url, params=query_dict)
#     print response.url
#     print (response.status_code, response.reason)
#     if response.status_code == 200:
#         content = response.json()
#         for article in content['articles']:
#             print article.keys()

