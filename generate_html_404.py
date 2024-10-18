import random
import requests
import os

# Fetch the latest XKCD comic number
def fetch_latest_comic_number():
    response = requests.get('https://xkcd.com/info.0.json')
    latest_comic_data = response.json()
    return latest_comic_data['num']

# Fetch a random XKCD comic
def fetch_random_comic():
    latest_comic_number = fetch_latest_comic_number()
    comic_id = random.randint(1, latest_comic_number)
    response = requests.get(f'https://xkcd.com/{comic_id}/info.0.json')
    if response.status_code == 200:
        return response.json()

# Generate HTML content with 404 page style for embedding the XKCD comic
def generate_html_404_style(comic_data):
    title = comic_data['title']
    img_url = comic_data['img']
    alt_text = comic_data['alt']
    comic_url = f"https://xkcd.com/{comic_data['num']}/"

    html_404_style = f"""
    <html>
      <head>
        <title>404 - The page you requested cannot be found | EPU-NTUA</title>
        <style>
          body {{
            font-family: Arial, sans-serif;
            background-color: #f0f0f0;
            color: #555;
            text-align: center;
            padding-top: 50px;
          }}
          .container {{
            max-width: 600px;
            margin: 0 auto;
            text-align: center;
          }}
          h1 {{
            font-size: 48px;
            margin-bottom: 20px;
            color: #333;
          }}
          p {{
            font-size: 18px;
            color: #777;
            margin-bottom: 30px;
          }}
          img {{
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
          }}
          .alt-text {{
            font-style: italic;
            color: #999;
            margin-top: 10px;
          }}
          .footer {{
            margin-top: 50px;
            font-size: 14px;
            color: #aaa;
          }}
          .footer a {{
            color: #555;
            text-decoration: none;
            transition: color 0.3s ease, border-bottom 0.3s ease;
            border-bottom: 2px solid transparent;
          }}
          .footer a:hover {{
            color: #222;
            border-bottom: 2px solid #222;
          }}
          .github-link {{
            margin-top: 20px;
            font-size: 16px;
            color: #555;
          }}
          .github-link a {{
            font-weight: bold;
            color: #336699;
            text-decoration: none;
            transition: color 0.3s ease, transform 0.3s ease;
          }}
          .github-link a:hover {{
            color: #003366;
            transform: scale(1.05);
          }}
          .github-logo {{
            vertical-align: middle;
            width: 20px;
            height: 20px;
            margin-left: 5px;
          }}
        </style>
      </head>
      <body>
        <div class="container">
          <h1>404 - Page Not Found</h1>
          <p>Oops! The page you're looking for cannot be found. Here's a random XKCD comic instead:</p>
          
          <div class="comic-container">
            <img id="comic-img" src="{img_url}" alt="{alt_text}">
            <p class="alt-text" id="comic-alt">{alt_text}</p>
          </div>

          <div class="footer">
            <p><a href="{comic_url}" style="color: #555; text-decoration: none;">View on XKCD #{comic_data['num']}</a></p>
            <p>Powered by: <a href="https://xkcd.com/"> XKCD</a> | 
                <a href="https://github.com/TzorAL/daily-random-xkcd" target="_blank">
                    <img class="github-logo" src="https://upload.wikimedia.org/wikipedia/commons/4/4a/GitHub_Mark.png" alt="GitHub Logo">
                </a>
            </p>
          </div>
        </div>
      </body>
    </html>
    """
    return html_404_style

# Save the HTML to a file in docs directory
def save_404_style_to_file(html_content):
    # Create the directory if it doesn't exist
    if not os.path.exists('docs'):
        os.makedirs('docs')
    
    # Save the HTML file to the 'docs' directory
    with open('docs/404/xkcd_404_style.html', 'w') as file:
        file.write(html_content)
        
# Main function to fetch a random XKCD comic and generate the HTML file
if __name__ == "__main__":
    comic_data = fetch_random_comic()
    html_404_style = generate_html_404_style(comic_data)
    save_404_style_to_file(html_404_style)
    print("xkcd_404_style.html has been generated.")
