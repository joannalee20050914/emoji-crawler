Emoji Crawler
Overview
This project is a Python web crawler designed to scrape emoji combinations and ASCII art from emojicombos.com. The website provides various emoji combos and ASCII art tagged with keywords, allowing users to search for emojis by tags like "happy," "cute," or "kitty."
As a beginner in programming, I wanted to practice web scraping with Python. The goal is to extract emoji combos and their associated tags, filter out unwanted content (e.g., creepy or unsettling emojis tagged with "weird"), and save the data into JSON files. Later, I plan to use this data with Grok (an AI assistant) to enhance conversations—Grok can respond with emoji combos matching the mood of the conversation (e.g., adding a "cheer" emoji when the mood is cheerful).
Features

Web Scraping: Uses Python libraries (requests, BeautifulSoup) to scrape emoji combos from multiple categories (e.g., "kawaii," "cute").
Filtering: Filters out emojis with English sentences and unwanted tags (e.g., "weird," "creepy").
Categorization: Saves emojis into separate JSON files based on themes (e.g., emotions, ASCII art).
Future Plan: Integrate with Grok to dynamically add emojis to responses based on conversational mood.

How It Works

The script scrapes emoji combos from emojicombos.com across specified categories.
It filters out unwanted emojis using criteria like:
English sentences (e.g., "why r we arguing").
Unwanted tags (e.g., "weird," "scary").


The filtered emojis are categorized into emotions (e.g., "happy," "sad") and ASCII art (e.g., "kitty") and saved into emotions.json and ascii.json.

Future Improvements

Add more categories and tags for filtering.
Improve filtering logic to handle edge cases.
Integrate with Grok for real-time emoji suggestions in conversations.

Getting Started

Clone the repository:
git clone https://github.com/你的用戶名/emoji-crawler.git


Install dependencies:
pip install requests beautifulsoup4


Run the script:
python findemoji.py


Check the output files: emotions.json and ascii.json.


