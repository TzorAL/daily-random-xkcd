import json
import random
import requests
import os

# Load seen comics from JSON file
def load_seen_comics():
    # Check if seen_comics.json exists
    if not os.path.exists('seen_comics.json'):
        # If it does not exist, create an empty seen_comics.json file
        with open('seen_comics.json', 'w') as file:
            json.dump([], file)
        return []
    
    # If it exists, load the seen comics
    try:
        with open('seen_comics.json', 'r') as file:
            return json.load(file)
    except json.JSONDecodeError:
        return []

# Save seen comics to JSON file
def save_seen_comics(seen_comics):
    with open('seen_comics.json', 'w') as file:
        json.dump(seen_comics, file)

# Fetch a random xkcd comic
def fetch_random_comic():
    total_comics = 2544  # Update this number with the latest xkcd comic number
    comic_id = random.randint(1, total_comics)
    response = requests.get(f'https://xkcd.com/{comic_id}/info.0.json')
    
    # Ensure the comic is not already seen
    seen_comics = load_seen_comics()
    while comic_id in seen_comics:
        comic_id = random.randint(1, total_comics)
        response = requests.get(f'https://xkcd.com/{comic_id}/info.0.json')
    
    return response.json()

# Generate RSS feed
def generate_rss():
    comic_data = fetch_random_comic()
    title = comic_data['title']
    img_url = comic_data['img']
    alt_text = comic_data['alt']
    
    rss_content = f"""<?xml version="1.0" encoding="UTF-8" ?>
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
    return rss_content

# Save the RSS feed to a file
def save_rss_to_file(rss_content):
    with open('xkcd_feed.xml', 'w') as file:
        file.write(rss_content)

# Main function to run the script
if __name__ == "__main__":
    rss_feed = generate_rss()
    save_rss_to_file(rss_feed)
    
    # Update the seen comics
    seen_comics = load_seen_comics()
    comic_data = json.loads(rss_feed).get('channel').get('item')[0]
    seen_comics.append(comic_data['guid'])
    save_seen_comics(seen_comics)
