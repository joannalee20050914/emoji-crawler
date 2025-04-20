import requests
from bs4 import BeautifulSoup
import json
import time
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
import re

# 設置 Selenium 為 Edge（macOS 環境）
edge_options = Options()
edge_options.add_argument("--headless")  # 無頭模式（不開瀏覽器窗口）
edge_options.add_argument("--disable-gpu")
service = Service("./msedgedriver")
driver = webdriver.Edge(service=service, options=edge_options)

# 定義基礎 URL
base_url = "https://emojicombos.com/"

# 定義已知的 emoji 類別（作為備用）
known_categories = [
    "kawaii", "cute", "sad", "happy", "love", "friends", "aesthetic", "playful", "capybara", "shy",
    "kitty", "cat", "dog", "bunny", "bear", "fox", "panda", "bird", "fish", "flower", "heart", "star"
]

# 改進類別提取邏輯
def get_all_categories():
    print("Fetching all categories...")
    driver.get(base_url)
    time.sleep(3)  # 等待頁面載入

    # 模擬滾動頁面以載入所有內容
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # 等待載入
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    soup = BeautifulSoup(driver.page_source, "html.parser")
    # 尋找所有 <a> 標籤，並過濾出可能的類別
    category_links = soup.find_all("a", href=re.compile(r'^/[a-zA-Z0-9-]+'))
    categories = set()
    for link in category_links:
        href = link.get("href")
        if href and href.startswith("/"):
            category = href[1:]  # 移除前面的 "/"
            # 過濾條件：排除無效類別
            if (category and not any(char in category for char in "?#") and
                "generator" not in category and "editor" not in category and
                "privacy" not in category and "terms" not in category and
                len(category.split("-")) <= 3):  # 限制類別名稱長度
                categories.add(category)
    
    # 如果抓到的類別太少，補充已知的類別
    categories_list = list(categories)
    if len(categories_list) < 10:
        print("Too few categories found, adding known categories...")
        categories_list.extend(known_categories)
        categories_list = list(set(categories_list))  # 去重

    return categories_list

# 獲取所有類別
categories = get_all_categories()
print(f"Found {len(categories)} categories: {categories[:10]}...")  # 顯示前 10 個類別

# 要保留的關鍵字
emotion_tags = [
    "happy", "joy", "cheer", "excited", "delight", "glad", "smile", "laugh", "fun", "yay", "celebrate", "party", "bliss",
    "thrilled", "ecstatic", "overjoyed", "gleeful", "merry", "cheerful", "sunny", "bright",
    "sad", "cry", "tear", "upset", "depressed", "heartbroken", "sorry", "melancholy", "grief", "sorrow", "blue",
    "miserable", "lonely", "down", "hurt", "weep", "despair", "forlorn", "gloomy",
    "angry", "mad", "annoyed", "frustrated", "irritated", "rage", "furious", "grumpy",
    "enraged", "irate", "outraged", "bitter", "resentful", "cross", "huffy",
    "surprised", "shock", "amazed", "astonished", "wow", "stunned",
    "bewildered", "flabbergasted", "dumbfounded", "startled", "speechless",
    "embarrassed", "awkward", "shy", "nervous", "oops", "helpless", "sigh", "blush", "timid",
    "clumsy", "uneasy", "sheepish", "fidgety", "restless", "meh", "whatever",
    "love", "heart", "kiss", "hug", "sweet", "romantic", "darling", "lover", "affection", "care",
    "passion", "adore", "cherish", "devotion", "soulmate", "sweetheart", "lovely",
    "friends", "friendship", "buddy", "pal", "mate", "bff", "bestie", "group", "team", "bond",
    "squad", "crew", "gang", "partner", "companion", "chum", "ally",
    "calm", "peace", "relax", "sleepy", "tired", "lazy", "bored", "confused", "curious", "proud", "hope", "dreamy",
    "anxious", "worried", "scared", "tense", "jealous", "envy", "grateful", "thankful", "content", "satisfied",
    "playful", "silly", "goofy", "mischievous", "naughty"
]

ascii_tags = [
    "kitty", "cat", "dog", "puppy", "bunny", "rabbit", "bear", "fox", "wolf", "deer", "panda", "hamster", "mouse", "bird",
    "fish", "duck", "chicken", "pig", "cow", "sheep", "horse",
    "lion", "tiger", "elephant", "giraffe", "zebra", "monkey", "koala", "kangaroo", "snake", "frog", "turtle",
    "dolphin", "whale", "shark", "octopus", "butterfly", "bee", "ladybug", "dragon", "unicorn", "mermaid",
    "ascii", "kaomoji", "text art", "symbol", "character", "face", "expression", "cute kaomoji",
    "flower", "heart", "star", "moon", "sun", "cloud", "tree", "food", "drink", "music", "note", "emoji", "emoticon", "smiley",
    "capybara"
]

# 不想要的標籤
unwanted_tags = [
    "weird", "creepy", "scary", "horror", "spooky", "eerie", "freaky", "gross", "disgusting", "bloody", "gore", "violent",
    "dark", "nightmare", "haunted", "ghost", "monster", "zombie", "skeleton", "demon", "devil", "vampire", "werewolf", "curse",
    "fear", "panic", "disturbing", "unsettling", "terrifying", "grim", "macabre", "sinister", "evil", "psycho", "insane",
    "madness", "death", "dead", "skull", "bones", "grave", "cemetery", "blood", "knife", "weapon", "murder", "kill",
    "bizarre", "odd", "strange", "frightening", "chilling", "dreadful", "ghastly", "horrific", "petrifying", "alarming",
    "shocking", "lurid", "morbid", "twisted", "warped",
    "slash", "stab", "wound", "injury", "brutal", "savage", "cruel", "torture", "pain", "scream", "agony", "slaughter",
    "massacre", "execution", "war", "battle", "fight", "punch", "kick",
    "uncomfortable", "gross", "nasty", "sick", "vomit", "rotten", "decay", "foul", "stink", "smelly", "disease", "infection",
    "parasite", "bug", "worm", "spider", "rat", "cockroach",
    "nsfw", "adult", "sexy", "nude", "lewd", "inappropriate", "offensive", "rude", "vulgar", "swear", "curse", "profanity",
    "hate", "racist", "sexist", "politics", "religion"
]

# 不想要的 emoji 內容關鍵詞
unwanted_content_keywords = [
    "http", "https", "www", "@", "user",
    "follow", "subscribe", "like", "comment", "post", "share", "bio", "profile", "status", "quote", "username",
    "discord", "insta", "instagram", "twitter", "tiktok", "snapchat", "remove this"
]

# 分開儲存的資料
emotion_data = []
ascii_data = []

# 篩選條件
MAX_EMOJI_LENGTH = 500

# 檢查英文單詞（3 個或以上連續字母）
def has_english_sentence(emoji_text):
    words = re.findall(r'\b[a-zA-Z]{3,}\b', emoji_text)
    return len(words) >= 2

# 檢查不想要的內容關鍵詞
def has_unwanted_content(emoji_text):
    emoji_text_lower = emoji_text.lower()
    return any(keyword in emoji_text_lower for keyword in unwanted_content_keywords)

# 改進標籤匹配邏輯（部分匹配）
def matches_tag(tags, target_tags):
    for tag in tags:
        tag_lower = tag.lower()
        for target in target_tags:
            if target in tag_lower:  # 部分匹配
                return True
    return False

for category in categories:
    url = base_url + category
    print(f"Fetching {url}...")
    try:
        driver.get(url)
        time.sleep(3)  # 等待頁面載入
        # 模擬滾動以載入更多內容
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # 等待滾動後載入
        soup = BeautifulSoup(driver.page_source, "html.parser")
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        continue

    combo_wrappers = soup.find_all("div", class_="combo-wrapper")

    print(f"Found {len(combo_wrappers)} combo wrappers in {category}")

    for wrapper in combo_wrappers:
        emoji_div = wrapper.find("div", class_="emojis")
        emoji_text = emoji_div.text if emoji_div else ""
        
        # 篩選條件
        if not emoji_text:
            print(f"Skipping empty emoji in {category}")
            continue
        
        if len(emoji_text) > MAX_EMOJI_LENGTH:
            print(f"Skipping long emoji: {emoji_text[:50]}...")
            continue
        
        if has_english_sentence(emoji_text):
            print(f"Skipping emoji with English sentence: {emoji_text[:50]}...")
            continue

        if has_unwanted_content(emoji_text):
            print(f"Skipping emoji with unwanted content: {emoji_text[:50]}...")
            continue

        keywords_div = wrapper.find("div", class_="keywords")
        tag_list = []
        if keywords_div:
            tags = keywords_div.find_all("a")
            tag_list = [tag.text.strip() for tag in tags]

        if any(unwanted_tag in tag_list for unwanted_tag in unwanted_tags):
            print(f"Skipping emoji with unwanted tags: {tag_list}")
            continue

        # 分類儲存（改進匹配邏輯）
        has_emotion = matches_tag(tag_list, emotion_tags)
        has_ascii = matches_tag(tag_list, ascii_tags)

        combo = {
            "emoji": emoji_text.strip(),
            "tags": tag_list,
            "category": category
        }

        if has_emotion:
            emotion_data.append(combo)
        if has_ascii:
            ascii_data.append(combo)

    time.sleep(1)

# 關閉瀏覽器
driver.quit()

print(f"Saved {len(emotion_data)} emotion emoji combinations")
print(f"Saved {len(ascii_data)} ASCII emoji combinations")

# 儲存到不同的 JSON 檔案
with open("emotions.json", "w", encoding="utf-8") as f:
    json.dump(emotion_data, f, ensure_ascii=False, indent=4)

with open("ascii.json", "w", encoding="utf-8") as f:
    json.dump(ascii_data, f, ensure_ascii=False, indent=4)

print("Emoji data saved to emotions.json and ascii.json")