# 🎲 Daily Random xkcd 🎲

## 📖 About
This repository **automatically generates a daily random xkcd comic** and serves it as an **RSS feed**. Each day, a new comic is fetched, formatted, and made available for subscription. Users can configure RSS feed reader to send email notifications whenever a new comic is available in the feed. It also features a fun xkcd-themed 404 error page that showcases a random comic in a playful layout.

---

## 🌟 Features
- 🕒 **Daily random xkcd comic fetching**.
- 📡 **Generates an RSS feed** that updates with new comic details.
- 🔄 **Tracks seen comics** to avoid duplicates via `seen_comics.json`.
- 🎨 **Custom xkcd 404 HTML page** showcasing a random comic in a unique format.

---

## ⚙️ How It Works
1. 🕔 **Daily Trigger**: A GitHub Actions workflow is triggered every day at **8:00 AM UTC+3** to run a Python script (`generate_rss.py`).
2. 📥 **Random Comic Fetch**: The script fetches a random comic from the xkcd API, ensuring it hasn't been seen before.
3. 📝 **XML Generation**: Comic details are formatted as XML and saved to `docs/xkcd_feed.xml`.
4. 🗂️ **Seen Comics Tracking**: The comics are tracked in `seen_comics.json` to avoid repeats.
5. 🚀 **RSS Hosting**: The RSS feed is hosted on GitHub for easy access by RSS web feeds.
6. 📧 **Email Notifications**: RSS feed reader monitors the feed and sends email alerts when a new comic is available.
7. 💡 **404 Page**: A Python script generates an xkcd-themed 404 page with a random comic.

---

## 🛠️ Getting Started

You can use this tool in two ways:

### 1. Use the Pre-Generated RSS Feed Hosted by GitHub

- Subscribe to the **[Daily Random XKCD RSS Feed](https://tzoral.github.io/daily-random-xkcd/docs/rss/xkcd_feed.xml)**.
- Optionally, configure email notifications via RSS feed readers or any other RSS service to receive daily updates whenever a new comic is available.

### 2. Fork the Repository and Automate Your Own Feed

If you'd like to run your own instance of this tool:

1. **Fork** this repository to your GitHub account.
2. **Enable GitHub Actions** in your forked repository.
3. **Set up RSS feed reader**:
   - Create a new RSS feed alert for the URL.
   - Configure email notifications based on your preferences.
4. Enjoy daily xkcd emails and check the latest comic each day.
5. Access the 404 Page whenever you want a random xkcd comic.

---

## 🔗 Links

- **🚧 [404 HTML Page](https://tzoral.github.io/daily-random-xkcd/docs/404/)**  
  *A beautifully styled 404 page demonstrating an XKCD comic*.

- **📡 [RSS Comic Feed](https://tzoral.github.io/daily-random-xkcd/docs/rss/xkcd_feed.xml)**  
  *An RSS feed of random XKCD comics, formatted in XML*.

---

## 📂 Files

- `generate_rss.py`: Python script to fetch a random xkcd comic, track seen comics, and generate the RSS feed.
- `generate_html_404_style_xkcd.py`: Python script to generate the random xkcd-themed 404 page.
- `seen_comics.json`: JSON file that tracks comics to prevent repeats.
- `docs/rss/xkcd_feed.xml`: RSS feed with the latest comic details.
- `docs/404/xkcd_404_style.html`: HTML file for the 404 page.
- `.github/workflows/update_xkcd_rss_feed.yaml`: GitHub Actions workflow to update the RSS feed daily.
- `.github/workflows/update_html_404.yaml`: GitHub Actions workflow to update the 404 page daily.

---

## 🔮 Future Expansion

We plan to expand this project to include **other webcomics** such as *Saturday Morning Breakfast Cereal* (SMBC). The vision includes:

- **Daily Fetching**: Automatically fetching a random SMBC comic each day, similar to the xkcd functionality.
- **Separate RSS Feeds**: Creating distinct RSS feeds for each comic to cater to different audiences.
- **Integration**: Providing a unified interface for users to subscribe to multiple comic feeds simultaneously.
- **Themed Error Pages**: Developing themed 404 pages for each comic style, making the error experience unique and enjoyable.

Stay tuned for updates as we explore these exciting new features!

---

## 📝 License
This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for more details.

---

## 🙏 Acknowledgements

- Thanks to [xkcd](https://xkcd.com/) for their amazing comics.
- Shoutout to [GitHub Actions](https://docs.github.com/en/actions) for making automation easy.
- Thanks to [Feedrabbit](https://feedrabbit.com/) for helping automate RSS-to-email services.

---

## 📬 Contact
If you have any questions or suggestions, feel free to **open an issue** in this repository!
