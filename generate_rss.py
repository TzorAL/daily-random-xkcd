import json
import random
import requests
import os
from datetime import datetime

# File path for storing seen comics
SEEN_COMICS_FILE = 'seen_comics.json'

# Load seen comics from a file
def load_seen_comics():
    if os.path.exists(SEEN_COMICS_FILE):
        with open(SEEN_COMICS_FILE, 'r') as file:
            return json.load(file)
    return []  # If the file doesn't exist, return an empty list

# Save seen comics to a file
def save_seen_comics(seen_comics):
    with open(SEEN_COMICS_FILE, 'w') as file:
        json.dump(seen_comics, file)

# Fetch the latest XKCD comic number
def fetch_latest_comic_number():
    try:
        response = requests.get('https://xkcd.com/info.0.json', timeout=5)
        response.raise_for_status()
        latest_comic_data = response.json()
        return latest_comic_data['num']
    except requests.RequestException as e:
        print(f"Error fetching latest comic: {e}")
        return None

# Fetch a random XKCD comic that hasn't been seen yet
def fetch_random_comic(seen_comics):
    latest_comic_number = fetch_latest_comic_number()
    if latest_comic_number is None:
        return None  # Exit if we can't fetch the latest comic number
    while True:
        comic_id = random.randint(1, latest_comic_number)
        if comic_id not in seen_comics:
            try:
                response = requests.get(f'https://xkcd.com/{comic_id}/info.0.json', timeout=5)
                response.raise_for_status()
                return response.json()
            except requests.RequestException as e:
                print(f"Error fetching comic #{comic_id}: {e}")
                continue

# Generate RSS feed
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

    rss_content = f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
  <channel>
    <title>[xkcd] Random Comic Feed</title>
    <link>https://xkcd.com/</link>
    <description>A feed of random xkcd comics.</description>
    <language>en-us</language>
    <copyright>xkcd.com</copyright>
    <lastBuildDate>{pub_date}</lastBuildDate>
    <item>
      <title>{title}</title>
      <link>https://xkcd.com/{comic_data['num']}/</link>
      <description>
        <![CDATA[
          <div style="font-family: Arial, sans-serif; background-color: #f9f9f9; color: #333; padding: 10px; border: 1px solid #ccc; border-radius: 5px;">
            <p style="font-style: italic; color: #666;">[<a href="https://xkcd.com/{comic_data['num']}/" style="color: #1a0dab; text-decoration: none;">#{comic_data['num']}</a>] {alt_text}</p>  <!-- Alt text added here -->
            <a href="{img_url}" style="color: #1a0dab; text-decoration: none;">
              <img src="{img_url}" alt="{alt_text}" style="max-width: 100%; height: auto; border-radius: 4px; margin-top: 10px;">
            </a>
          </div>
        ]]>
      </description>
      <guid isPermaLink="true">https://xkcd.com/{comic_data['num']}/</guid>
      <pubDate>{comic_data['year']}-{comic_data['month']}-{comic_data['day']}</pubDate>
    </item>
  </channel>
</rss>
"""
    return rss_content

# Save the RSS feed to a file
def save_rss_to_file(rss_content):
    if rss_content:
        with open('docs/xkcd_feed.xml', 'w') as file:
            file.write(rss_content)
    else:
        print("Failed to generate RSS feed.")

# Main function to run the script
if __name__ == "__main__":
    rss_feed = generate_rss()
    save_rss_to_file(rss_feed)
