import os
import json
import random
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# File to store the list of seen comics
SEEN_COMICS_FILE = 'seen_comics.json'

# Initialize seen_comics.json if it doesn't exist
if not os.path.exists(SEEN_COMICS_FILE):
    with open(SEEN_COMICS_FILE, 'w') as file:
        json.dump([], file)  # Initialize with an empty list

def load_seen_comics():
    """Load the list of seen comics from the JSON file."""
    if os.path.exists(SEEN_COMICS_FILE):
        try:
            with open(SEEN_COMICS_FILE, 'r') as file:
                return json.load(file)
        except json.JSONDecodeError:
            return []  # Return an empty list if JSON is invalid
    else:
        return []

def save_seen_comics(seen_comics):
    """Save the list of seen comics to the JSON file."""
    with open(SEEN_COMICS_FILE, 'w') as file:
        json.dump(seen_comics, file)

def fetch_random_comic():
    """Fetch a random xkcd comic."""
    response = requests.get('https://xkcd.com/info.0.json')
    total_comics = response.json()['num']
    
    seen_comics = load_seen_comics()
    unseen_comics = [i for i in range(total_comics + 1) if i not in seen_comics]

    if not unseen_comics:
        # If all comics have been seen, reset the seen list
        unseen_comics = list(range(total_comics + 1))
        seen_comics = []

    random_comic_id = random.choice(unseen_comics)
    comic_url = f'https://xkcd.com/{random_comic_id}/info.0.json'
    comic_response = requests.get(comic_url).json()

    # Update the seen comics
    seen_comics.append(random_comic_id)
    save_seen_comics(seen_comics)

    return comic_response['title'], comic_response['img'], comic_response['alt']

def send_email(subject, body, to_email, smtp_server, smtp_port, email_address, email_password):
    """Send an email with the specified subject and body."""
    print(f"Sending email to: {to_email}")  # Debugging line
    msg = MIMEMultipart()
    msg['From'] = email_address
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'html'))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Secure the connection
            server.login(email_address, email_password)
            server.send_message(msg)
            print("Email sent successfully!")  # Debugging line
    except Exception as e:
        print(f"Failed to send email: {e}")  # Print any errors that occur

def main():
    # Fetch a random unseen comic
    title, img_url, alt_text = fetch_random_comic()

    # Prepare email content
    subject = f"xkcd Comic: {title}"
    body = f'<h1>{title}</h1><img src="{img_url}" alt="{alt_text}"><p>{alt_text}</p>'

    # Email credentials and settings
    to_email = os.environ['EMAIL_ADDRESS']  # Your email address to send to
    smtp_server = os.environ['SMTP_SERVER']
    smtp_port = os.environ['SMTP_PORT']
    email_password = os.environ['EMAIL_PASSWORD']

    # Send the email
    send_email(subject, body, to_email, smtp_server, smtp_port, to_email, email_password)

    # Commit and push the seen_comics.json file
    email_address = os.environ['EMAIL_ADDRESS']  # Get email address from secrets
    os.system(f"git config --global user.email '{email_address}'")  # Use the email from secrets
    os.system("git config --global user.name 'GitHub Actions'")  # Use a generic name
    os.system("git add seen_comics.json")
    os.system("git commit -m 'Update seen comics'")
    os.system("git push origin main")

if __name__ == '__main__':
    main()
