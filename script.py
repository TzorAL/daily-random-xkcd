import os
import json
import random
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def load_seen_comics(filename='seen_comics.json'):
    """Load the list of seen comics from a JSON file."""
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return json.load(file)
    return []

def save_seen_comics(comics, filename='seen_comics.json'):
    """Save the list of seen comics to a JSON file."""
    with open(filename, 'w') as file:
        json.dump(comics, file)

def fetch_random_comic():
    """Fetch a random xkcd comic that hasn't been seen before."""
    seen_comics = load_seen_comics()
    
    # Total number of xkcd comics
    total_comics = 2544  # Update this number based on the latest xkcd comics
    unseen_comics = list(set(range(total_comics)) - set(seen_comics))

    if not unseen_comics:
        # If all comics have been seen, reset the seen_comics.json
        unseen_comics = list(range(total_comics))
        save_seen_comics([])

    comic_id = random.choice(unseen_comics)
    response = requests.get(f'https://xkcd.com/{comic_id}/info.0.json')
    comic_data = response.json()

    # Update seen comics
    seen_comics.append(comic_id)
    save_seen_comics(seen_comics)

    return comic_data['title'], comic_data['img'], comic_data['alt']

def send_email(subject, body, to_email, smtp_server, smtp_port, email_address, email_password):
    """Send an email with the specified subject and body."""
    print(f"Sending email to: {to_email}")  # Debugging line
    print(f"SMTP Server: {smtp_server}, SMTP Port: {smtp_port}")  # Debugging line

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

    # Email credentials and settings from environment variables
    to_email = os.environ['EMAIL_ADDRESS']  # Your email address to send to
    smtp_server = os.environ['SMTP_SERVER']
    smtp_port = os.environ['SMTP_PORT']
    email_password = os.environ['EMAIL_PASSWORD']

    # Send the email
    send_email(subject, body, to_email, smtp_server, smtp_port, to_email, email_password)

    # Commit and push the seen_comics.json file using GITHUB_TOKEN
    os.system("git config --global user.name 'GitHub Actions'")
    os.system("git config --global user.email 'actions@github.com'")
    os.system("git add seen_comics.json")
    os.system("git commit -m 'Update seen comics'")
    os.system("git push https://x-access-token:${{ secrets.GITHUB_TOKEN }}@github.com/TzorAL/daily-random-xkcd.git HEAD:main")

if __name__ == '__main__':
    main()
