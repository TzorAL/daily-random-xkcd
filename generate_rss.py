import json
import random
import requests
import os
import time
from datetime import datetime

SEEN_COMICS_FILE = 'seen_comics.json'

def load_seen_comics():
    if os.path.exists(SEEN_COMICS_FILE):
        with open(SEEN_COMICS_FILE, 'r') as file:
            return json.load(file)
    return []

def save_seen_comics(seen_comics):
    with open(SEEN_COMICS_FILE, 'w') as file:
        json.dump(seen_comics, file)

def fetch_latest_comic_number():
    try:
        response = requests.get('https://xkcd.com/info.0.json', timeout=5)
        response.raise_for_status()
        latest_comic_data = response.json()
        return latest_comic_data['num']
    except requests.RequestException as e:
        print(f"Error fetching latest comic: {e}")
        return None

def clear_seen_comics_if_complete(seen_comics, latest_comic_number, reset=False):
    if reset and len(seen_comics) >= latest_comic_number:
        print("All comics have been seen. Clearing the seen comics list.")
        seen_comics.clear()
        save_seen_comics(seen_comics)

def fetch_random_comic(seen_comics):
    latest_comic_number = fetch_latest_comic_number()
    if latest_comic_number is None:
        return None

    clear_seen_comics_if_complete(seen_comics, latest_comic_number)

    attempts = 0
    max_attempts = 10

    while attempts < max_attempts:
        comic_id = random.randint(1, latest_comic_number)
        if comic_id not in seen_comics:
            try:
                response = requests.get(f'https://xkcd.com/{comic_id}/info.0.json', timeout=5)
                response.raise_for_status()
                return response.json()
            except requests.RequestException as e:
                print(f"Error fetching comic #{comic_id}: {e}")
                attempts += 1
                time.sleep(1)
                continue

    print("Max attempts reached. No unseen comics available.")
    return None

def generate_rss():
    seen_comics = load_seen_comics()
    comic_data = fetch_random_comic(seen_comics)
    if comic_data is None:
        return None  # Exit if we couldn't fetch a random comic

    # Update the seen comics list
    seen_comics.append(comic_data['num'])
    save_seen_comics(seen_comics)

    title = comic_data['title']
    img_url = comic_data['img']
    alt_text = comic_data['alt']
    pub_date = datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT")
    formatted_pub_date = f"{comic_data['year']}-{int(comic_data['month']):02d}-{int(comic_data['day']):02d}"

    rss_content = f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>[xkcd] Random Comic Feed</title>
    <link>https://xkcd.com/</link>
    <description>A feed of random xkcd comics.</description>
    <language>en-us</language>
    <copyright>xkcd.com</copyright>
    <lastBuildDate>{pub_date}</lastBuildDate>
    <atom:link href="https://xkcd.com/" rel="self" type="application/rss+xml" />
    <item>
      <title>{title}</title>
      <link>https://xkcd.com/{comic_data['num']}/</link>
      <description>
        <![CDATA[
          <div>
            <p>[<a href="https://xkcd.com/{comic_data['num']}/">#{comic_data['num']}</a>] {alt_text}</p>
            <a href="{img_url}">
              <img src="{img_url}" alt="{alt_text}" style="max-width: 100%; height: auto;" />
            </a>
          </div>
        ]]>
      </description>
      <guid isPermaLink="true">https://xkcd.com/{comic_data['num']}/</guid>
      <pubDate>{formatted_pub_date}</pubDate>
    </item>
  </channel>
</rss>
"""
    return rss_content

def save_rss_to_file(rss_content):
    os.makedirs('docs/rss', exist_ok=True)

    if rss_content:
        with open('docs/rss/xkcd_feed.xml', 'w') as file:
            file.write(rss_content)
    else:
        print("Failed to generate RSS feed.")

if __name__ == "__main__":
    rss_feed = generate_rss()
    save_rss_to_file(rss_feed)
