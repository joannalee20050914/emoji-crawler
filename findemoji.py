import requests
from bs4 import BeautifulSoup
import json
import time
import re

# 定義多個類別
categories = ["kawaii", "cute", "sad", "happy", "love"]
base_url = "https://emojicombos.com/"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

emoji_data = []

# 篩選條件
MAX_EMOJI_LENGTH = 50  # 最大長度限制

# 檢查英文單詞（3 個或以上連續字母）
def has_english_sentence(emoji_text):
    # 尋找所有 3 個或以上連續字母的單詞
    words = re.findall(r'\b[a-zA-Z]{3,}\b', emoji_text)
    # 如果有 2 個或以上單詞，視為句子
    return len(words) >= 2

for category in categories:
    url = base_url + category
    print(f"Fetching {url}...")
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        continue

    soup = BeautifulSoup(response.text, "html.parser")
    combo_wrappers = soup.find_all("div", class_="combo-wrapper")

    print(f"Found {len(combo_wrappers)} combo wrappers in {category}")

    for wrapper in combo_wrappers:
        emoji_div = wrapper.find("div", class_="emojis")
        emoji_text = emoji_div.text if emoji_div else ""
        
        # 篩選條件
        if not emoji_text:  # 跳過空的 emoji
            continue
        
        # 檢查長度
        if len(emoji_text) > MAX_EMOJI_LENGTH:
            print(f"Skipping long emoji: {emoji_text[:50]}...")
            continue
        
        # 檢查是否有英文句子
        if has_english_sentence(emoji_text):
            print(f"Skipping emoji with English sentence: {emoji_text[:50]}...")
            continue

        keywords_div = wrapper.find("div", class_="keywords")
        tag_list = []
        if keywords_div:
            tags = keywords_div.find_all("a")
            tag_list = [tag.text.strip() for tag in tags]

        if "weird" not in tag_list:
            emoji_data.append({
                "emoji": emoji_text.strip(),
                "tags": tag_list,
                "category": category
            })

    # 添加延遲，避免過快請求
    time.sleep(1)

print(f"Saved {len(emoji_data)} emoji combinations")

with open("emoji_data.json", "w", encoding="utf-8") as f:
    json.dump(emoji_data, f, ensure_ascii=False, indent=4)

print("Emoji data saved to emoji_data.json")