import requests
from bs4 import BeautifulSoup
import json
import time
import re

# 定義多個類別
categories = ["kawaii", "cute", "sad", "happy", "love", "friends", "aesthetic", "playful"]
base_url = "https://emojicombos.com/"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

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
    "capybara", "kitty", "cat", "dog", "puppy", "bunny", "rabbit", "bear", "fox", "wolf", "deer", "panda", "hamster", "mouse", "bird",
    "fish", "duck", "chicken", "pig", "cow", "sheep", "horse",
    "lion", "tiger", "elephant", "giraffe", "zebra", "monkey", "koala", "kangaroo", "snake", "frog", "turtle",
    "dolphin", "whale", "shark", "octopus", "butterfly", "bee", "ladybug", "dragon", "unicorn", "mermaid",
    "ascii", "kaomoji", "text art", "symbol", "character", "face", "expression", "cute kaomoji",
    "flower", "heart", "star", "moon", "sun", "cloud", "tree", "food", "drink", "music", "note", "emoji", "emoticon", "smiley"
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
    "sorry", "apology", "please", "thanks", "thank you", "http", "https", "www", "@", "user",
    "follow", "subscribe", "like", "comment", "post", "share", "bio", "profile", "status", "quote", "username",
    "discord", "insta", "instagram", "twitter", "tiktok", "snapchat", "made by", "created by", "credit", "remove this"
]

# 分開儲存的資料
emotion_data = []
ascii_data = []

# 篩選條件
MAX_EMOJI_LENGTH = 50  # 最大長度限制

# 檢查英文單詞（3 個或以上連續字母）
def has_english_sentence(emoji_text):
    words = re.findall(r'\b[a-zA-Z]{3,}\b', emoji_text)
    return len(words) >= 2

# 檢查不想要的內容關鍵詞
def has_unwanted_content(emoji_text):
    emoji_text_lower = emoji_text.lower()
    return any(keyword in emoji_text_lower for keyword in unwanted_content_keywords)

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

        # 檢查是否有不想要的內容關鍵詞
        if has_unwanted_content(emoji_text):
            print(f"Skipping emoji with unwanted content: {emoji_text[:50]}...")
            continue

        keywords_div = wrapper.find("div", class_="keywords")
        tag_list = []
        if keywords_div:
            tags = keywords_div.find_all("a")
            tag_list = [tag.text.strip() for tag in tags]

        # 檢查不想要的標籤
        if any(unwanted_tag in tag_list for unwanted_tag in unwanted_tags):
            print(f"Skipping emoji with unwanted tags: {tag_list}")
            continue

        # 分類儲存
        # 檢查是否包含情緒標籤
        has_emotion = any(emotion_tag in tag_list for emotion_tag in emotion_tags)
        # 檢查是否包含 ASCII 標籤
        has_ascii = any(ascii_tag in tag_list for ascii_tag in ascii_tags)

        combo = {
            "emoji": emoji_text.strip(),
            "tags": tag_list,
            "category": category
        }

        if has_emotion:
            emotion_data.append(combo)
        if has_ascii:
            ascii_data.append(combo)

    # 添加延遲，避免過快請求
    time.sleep(1)

print(f"Saved {len(emotion_data)} emotion emoji combinations")
print(f"Saved {len(ascii_data)} ASCII emoji combinations")

# 儲存到不同的 JSON 檔案
with open("emotions.json", "w", encoding="utf-8") as f:
    json.dump(emotion_data, f, ensure_ascii=False, indent=4)

with open("ascii.json", "w", encoding="utf-8") as f:
    json.dump(ascii_data, f, ensure_ascii=False, indent=4)

print("Emoji data saved to emotions.json and ascii.json")