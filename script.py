import random
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
import os

# File to store the list of seen comics
SEEN_COMICS_FILE = 'seen_comics.json'

# Email configuration from environment variables
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
TO_EMAIL = 'recipient-email@example.com'  # Update this to your recipient's email

# Get the latest xkcd comic number
def get_latest_comic_num():
    latest_comic_url = "https://xkcd.com/info.0.json"
    latest_comic = requests.get(latest_comic_url).json()
    return latest_comic['num']

# Load the list of seen comics from a file
def load_seen_comics():
    if os.path.exists(SEEN_COMICS_FILE):
        with open(SEEN_COMICS_FILE, 'r') as file:
            return json.load(file)
    else:
        return []

# Save the list of seen comics to a file
def save_seen_comics(seen_comics):
    with open(SEEN_COMICS_FILE, 'w') as file:
        json.dump(seen_comics, file)

# Get a random xkcd comic that hasn't been seen yet
def get_random_unseen_comic():
    latest_comic_num = get_latest_comic_num()
    seen_comics = load_seen_comics()

    # If all comics have been seen, reset the seen list
    if len(seen_comics) >= latest_comic_num:
        seen_comics = []

    # Create a list of unseen comics
    unseen_comics = set(range(1, latest_comic_num + 1)) - set(seen_comics)

    # Choose a random unseen comic
    random_comic_num = random.choice(list(unseen_comics))
    random_comic_url = f"https://xkcd.com/{random_comic_num}/info.0.json"
    random_comic = requests.get(random_comic_url).json()

    # Add the comic to the seen list and save the updated list
    seen_comics.append(random_comic_num)
    save_seen_comics(seen_comics)

    return {
        'title': random_comic['title'],
        'img_url': random_comic['img'],
        'alt_text': random_comic['alt'],
        'comic_url': f"https://xkcd.com/{random_comic_num}"
    }

# Send the email with the random xkcd comic
def send_email(comic):
    # Set up the email content
    message = MIMEMultipart("alternative")
    message["Subject"] = f"Your Daily Random xkcd Comic: {comic['title']}"
    message["From"] = EMAIL_ADDRESS
    message["To"] = TO_EMAIL

    # HTML content for the email
    html_content = f"""
    <html>
    <body>
        <h1>{comic['title']}</h1>
        <p>
            <img src="{comic['img_url']}" alt="{comic['alt_text']}"/><br/>
            <i>{comic['alt_text']}</i>
        </p>
        <p><a href="{comic['comic_url']}">View on xkcd</a></p>
    </body>
    </html>
    """

    # Attach the HTML content to the email
    part = MIMEText(html_content, "html")
    message.attach(part)

    # Send the email using SMTP
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, TO_EMAIL, message.as_string())
        print(f"Email sent to {TO_EMAIL} successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")
    finally:
        server.quit()

# Main logic
comic = get_random_unseen_comic()
send_email(comic)
