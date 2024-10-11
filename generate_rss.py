import json
import random
import requests
import os
import datetime

# Fetch a random xkcd comic
def fetch_random_comic():
    total_comics = 2544  # Update this number with the latest xkcd comic number
    comic_id = random.randint(1, total_comics)
    response = requests.get(f'https://xkcd.com/{comic_id}/info.0.json')
    return response.json()

# Generate RSS feed
def generate_rss(new_comic):
    title = new_comic['title']
    img_url = new_comic['img']
    alt_text = new_comic['alt']

    # Construct the new item for the RSS feed
    new_item = f"""<item>
      <title>{title}</title>
      <link>https://xkcd.com/{new_comic['num']}/</link>
      <description>
        <![CDATA[
          <div style="font-family: Arial, sans-serif; background-color: #f9f9f9; color: #333; padding: 10px; border: 1px solid #ccc; border-radius: 5px;">
            <h2 style="color: #2c3e50;">📢 New xkcd Comic Released!</h2>
            <h3>{title}</h3>
            <p style="margin: 10px 0;">Check out the latest xkcd comic below:</p>
            <a href="https://xkcd.com/{new_comic['num']}/" style="display: inline-block; padding: 10px 15px; background-color: #3498db; color: white; text-decoration: none; border-radius: 5px;">View Comic</a>
            <img src="{img_url}" alt="{alt_text}" style="max-width: 100%; height: auto; border-radius: 4px; margin-top: 10px;">
            <p style="font-style: italic; color: #666;">{alt_text}</p>
          </div>
        ]]>
      </description>
      <guid isPermaLink="true">https://xkcd.com/{new_comic['num']}/</guid>
      <pubDate>{new_comic['year']}-{new_comic['month']}-{new_comic['day']}</pubDate>
    </item>
    """
    
    return new_item

# Load existing RSS feed
def load_existing_rss():
    try:
        with open('xkcd_feed.xml', 'r') as file:
            return file.read()
    except FileNotFoundError:
        # If the file doesn't exist, return an empty string
        return ""

# Save the RSS feed to a file
def save_rss_to_file(rss_content):
    with open('xkcd_feed.xml', 'w') as file:
        file.write(rss_content)

# Main function to run the script
if __name__ == "__main__":
    # Fetch a new comic
    new_comic = fetch_random_comic()
    
    # Load existing RSS feed
    existing_rss = load_existing_rss()

    # Generate new item
    new_item = generate_rss(new_comic)

    # Check if the RSS feed is empty and format accordingly
    if existing_rss.strip() == "":
        rss_feed = f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
  <channel>
    <title>xkcd Random Comic</title>
    <link>https://xkcd.com/</link>
    <description>Random xkcd comic</description>
    {new_item}
  </channel>
</rss>
"""
    else:
        # Append the new item to the existing feed
        rss_feed = existing_rss.strip().replace("</channel>", f"{new_item}</channel>")

    # Save the updated RSS feed
    save_rss_to_file(rss_feed)
