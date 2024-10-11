# Daily Random xkcd

## About
This repository generates a daily random xkcd comic and serves it as an RSS feed. Each day, a new comic is fetched, formatted, and made available for subscription. Users can configure IFTTT to send email notifications whenever a new comic is available in the RSS feed.

## Features
- Automatically fetches a random xkcd comic daily.
- Generates an RSS feed that updates with new comic details.
- Sends email notifications via IFTTT whenever a new comic is published.

## How It Works
1. A GitHub Actions workflow is triggered daily at 8:00 AM UTC+3 to run a Python script (`generate_rss.py`).
2. The script fetches a random comic from the xkcd API.
3. The comic details are formatted in an XML structure and saved to `xkcd_feed.xml`.
4. The RSS feed is hosted on GitHub, allowing easy access for IFTTT.
5. An IFTTT applet monitors the RSS feed and sends an email whenever a new comic is detected.

## Setup Instructions
1. **Fork this repository** to your own GitHub account.
2. **Enable GitHub Actions** in your forked repository.
3. **Set up IFTTT**:
   - Create a new applet: "If New feed item from RSS feed, then Send yourself an email."
   - Use the RSS feed URL: `https://raw.githubusercontent.com/{your_username}/daily-random-xkcd/main/xkcd_feed.xml`
4. **Watch for daily emails** containing the latest xkcd comic!

## Files
- `generate_rss.py`: Python script that fetches a random xkcd comic and generates the RSS feed.
- `.github/workflows/main.yaml`: GitHub Actions workflow configuration that schedules the daily comic update.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements
- [xkcd](https://xkcd.com/) for providing a wealth of comics.
- [GitHub Actions](https://docs.github.com/en/actions) for enabling automated workflows.
- [IFTTT](https://ifttt.com/) for allowing simple automation of tasks based on web triggers.

## Contact
For questions or suggestions, feel free to open an issue in this repository.
