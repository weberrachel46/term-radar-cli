import requests
import re
from datetime import date

# Demo: scan Hacker News front page for new AI-related terms
HN_TOP = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM = "https://hacker-news.firebaseio.com/v0/item/{}.json"

AI_KEYWORDS = ["AI", "LLM", "model", "agent", "GPT", "neural", "deep learning"]

def fetch_json(url):
    try:
        r = requests.get(url, timeout=5)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def extract_terms(title):
    # crude extraction: words starting with uppercase or containing digits, plus AI context
    words = re.findall(r'\b[A-Z][a-zA-Z0-9_]+\b', title)
    terms = []
    for w in words:
        # filter out common words
        if w.lower() not in ["ai", "the", "a", "on", "for", "new", "how", "why"]:
            # check if title contains AI keywords
            if any(kw.lower() in title.lower() for kw in AI_KEYWORDS):
                terms.append(w)
    return terms

def main():
    print(f"=== AI Term Radar for {date.today()} ===")
    top_ids = fetch_json(HN_TOP)
    if not top_ids:
        return
    seen = set()
    count = 0
    for story_id in top_ids[:30]:
        story = fetch_json(ITEM.format(story_id))
        if not story or "title" not in story:
            continue
        title = story["title"]
        terms = extract_terms(title)
        for term in terms:
            if term not in seen:
                seen.add(term)
                print(f"- {term}")
                count += 1
                if count >= 10:
                    print("\n(First 10 new terms shown)")
                    return

if __name__ == "__main__":
    main()
