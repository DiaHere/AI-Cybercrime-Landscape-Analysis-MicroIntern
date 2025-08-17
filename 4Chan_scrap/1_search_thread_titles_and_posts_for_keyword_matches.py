import os
import json
import requests
from datetime import datetime
from bs4 import BeautifulSoup

# === CONFIG ===
BASE_DIR = "data/boards"
TODAY_DATE = datetime.now().strftime("%m%d%Y")
LOCAL_JSON_FILE = f"{BASE_DIR}/4chan_boards_{TODAY_DATE}.json"


def load_boards():
    if not os.path.exists(LOCAL_JSON_FILE):
        raise FileNotFoundError(f"Boards file not found: {LOCAL_JSON_FILE}. Run the download script first.")

    with open(LOCAL_JSON_FILE, "r", encoding="utf-8") as file:
        return json.load(file)["boards"]


def fetch_board_catalog(board_code):
    url = f"https://a.4cdn.org/{board_code}/catalog.json"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def clean_html(raw_html):
    if not raw_html:
        return ""
    soup = BeautifulSoup(raw_html, "html.parser")
    return soup.get_text(separator=" ").strip()


def search_keywords_in_board(board_code, board_title, keywords):
    print(f"[INFO] Searching /{board_code}/ - {board_title}")
    try:
        catalog = fetch_board_catalog(board_code)
    except Exception as e:
        print(f"[ERROR] Failed to fetch /{board_code}/: {e}")
        return []

    matches = []

    for page in catalog:
        for thread in page.get("threads", []):
            thread_title = clean_html(thread.get("sub", ""))
            thread_text = clean_html(thread.get("com", ""))
            content = f"{thread_title} {thread_text}".lower()

            for kw in keywords:
                if kw.lower() in content:
                    matches.append({
                        "Board": board_code,
                        "Thread ID": thread.get("no"),
                        "Title": thread_title,
                        "Text": thread_text,
                        "Matched Keyword": kw
                    })
                    break  # avoid duplicate matches on multiple keywords

    print(f"[INFO] Found {len(matches)} matches on /{board_code}/")
    return matches


def main():
    print("=== 4chan Keyword Search ===")
    keyword_input = input("Enter keyword(s) separated by commas (e.g., AI tools): ").strip()
    keywords = [kw.strip() for kw in keyword_input.split(",") if kw.strip()]
    if not keywords:
        print("[ERROR] No keywords entered. Exiting.")
        return

    boards = load_boards()
    all_matches = []

    for board in boards:
        board_code = board["board"]
        board_title = board["title"]
        matches = search_keywords_in_board(board_code, board_title, keywords)
        all_matches.extend(matches)

    print(f"\n✅ Done. Total matches across all boards: {len(all_matches)}")
    # Optionally: Save results to file
    # with open(f"{BASE_DIR}/search_results_{TODAY_DATE}.json", "w", encoding="utf-8") as f:
    #     json.dump(all_matches, f, indent=2)

    # Optional: print sample matches
    if all_matches:
        print("\n📌 Sample match:")
        print(json.dumps(all_matches[0], indent=2))


if __name__ == "__main__":
    main()
