import json
import random
import requests
from flask import Flask, jsonify, Response

app = Flask(__name__)

# Number of xkcd comics (this can be updated if new comics are released)
TOTAL_COMICS = 2544

def fetch_random_comic():
    """Fetch a random xkcd comic."""
    comic_id = random.randint(1, TOTAL_COMICS)
    response = requests.get(f'https://xkcd.com/{comic_id}/info.0.json')
    return response.json()

@app.route('/rss', methods=['GET'])
def rss_feed():
    """Generate an RSS feed for a random xkcd comic."""
    comic_data = fetch_random_comic()
    title = comic_data['title']
    img_url = comic_data['img']
    alt_text = comic_data['alt']

    rss = f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
  <channel>
    <title>xkcd Random Comic</title>
    <link>https://xkcd.com/</link>
    <description>Random xkcd comic</description>
    <item>
      <title>{title}</title>
      <link>https://xkcd.com/{comic_data['num']}/</link>
      <description><![CDATA[<img src="{img_url}" alt="{alt_text}"/><br>{alt_text}]]></description>
      <guid isPermaLink="true">https://xkcd.com/{comic_data['num']}/</guid>
      <pubDate>{comic_data['year']}-{comic_data['month']}-{comic_data['day']}</pubDate>
    </item>
  </channel>
</rss>
"""
    return Response(rss, mimetype='application/rss+xml')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
