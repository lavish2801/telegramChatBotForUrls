import re
import webbrowser
from telethon import TelegramClient, events

# ========= 1) FILL THESE FROM my.telegram.org =========
API_ID = 20155781
API_HASH = "db6f5a870fb42e682ba7e8d9e4e9cec0"

# ========= 2) CHOOSE YOUR TARGET CHAT =========
# Option A: A public group by username, e.g. "@mypublicgroup"
# Option B: A numeric chat ID for private groups (we'll discover it below)
TARGET_CHAT =None   # e.g. "@mypublicgroup"
# TARGET_CHAT = -1001234567890         # example numeric ID for a private group

# ========= 3) SETTINGS =========
# If a single message has multiple YouTube links, open all of them?
OPEN_ALL_LINKS_IN_MESSAGE = True

# Regex to catch both youtube.com and youtu.be links
YOUTUBE_URL_PATTERN = re.compile(
    r"https?://(?:www\.)?(?:youtube\.com/[^\s]+|youtu\.be/[^\s]+)",
    re.IGNORECASE
)

# Use a persistent local session so you don't log in every time
SESSION_NAME = "tg_youtube_opener_session"


def extract_youtube_urls(text: str):
    if not text:
        return []
    # Find all matching URLs
    urls = YOUTUBE_URL_PATTERN.findall(text)
    # Deduplicate while preserving order
    seen = set()
    unique = []
    for u in urls:
        if u not in seen:
            seen.add(u)
            unique.append(u)
    return unique


async def print_discovery_info(event):
    """
    Helper: If TARGET_CHAT is None, we print chat id & title of any incoming message.
    This helps you find the numeric id of private groups.
    """
    chat = await event.get_chat()
    try:
        chat_title = getattr(chat, "title", None) or getattr(chat, "first_name", None) or "Unknown"
        print(f"Discovered chat -> title: {chat_title!r}, id: {event.chat_id}")
    except Exception as e:
        print("Could not read chat info:", e)


def main():
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

    @client.on(events.NewMessage(chats=TARGET_CHAT if TARGET_CHAT else None))
    async def handler(event):
        # If TARGET_CHAT is None, we are in discovery mode
        if not TARGET_CHAT:
            await print_discovery_info(event)
            return

        text = event.message.message or ""
        urls = extract_youtube_urls(text)

        if not urls:
            return

        if OPEN_ALL_LINKS_IN_MESSAGE:
            for url in urls:
                print(f"[OPEN] {url}")
                webbrowser.open(url)
        else:
            print(f"[OPEN] {urls[0]}")
            webbrowser.open(urls[0])

    print("Starting Telegram client...")
    client.start()  # First run: will prompt for your phone & login code in console
    if not TARGET_CHAT:
        print("Discovery mode: send a message in the group you care about; watch this console for its ID.")
    else:
        print(f"Listening for YouTube links in: {TARGET_CHAT}")
    print("Press Ctrl+C to stop.")
    client.run_until_disconnected()


if __name__ == "__main__":
    main()
