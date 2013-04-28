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
    news_clips = []

    fr_resp = requests.get('http://api.flickr.com/services/rest/', params=payload)
    news_response = requests.get("http://bbc.api.mashery.com/juicer-ld-api/articles.json?binding=a&limit=5&where=%3Fa+cwork%3Atag+%3Fthing+.+%3Fa+%3Chttp%3A%2F%2Fwww.ontotext.com%2Fowlim%2Flucene%23articles%3E+%22crime+OR+murder%22+.+%3Chttp%3A%2F%2Fdbpedia.org%2Fresource%2FLondon%3E+geo-pos%3Alat+%3Flat+.+%3Chttp%3A%2F%2Fdbpedia.org%2Fresource%2FLondon%3E+geo-pos%3Along+%3Flong+.+%3Fthing+omgeo%3Anearby%28%3Flat+%3Flong+%2225mi%22%29+.&api_key=kzjvv89zfh43zjcz6gdhjcd3")

    if fr_resp.status_code == 200:
        fr_photo_set = json.loads(fr_resp.content[14:-1])
        photos = fr_photo_set['photos']['photo']

        for photo in photos:
            flickr_photos.append('http://farm9.staticflickr.com/{0}/{1}_{2}_q.jpg'.format(photo['server'], photo['id'], photo['secret']))
    
    if news_response.status_code == 200:
        news_content = news_response.json()
        for article in news_content['articles']:
            news_clips.append(
                {'description': article['description'],
                'title': article['title'],
                'url': article['url'],
                'highlight': article['highlight']})

    return jsonify({'data': flickr_photos, 'news': news_clips})

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()


