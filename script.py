import re
import asyncio
import random
import os
from telethon import TelegramClient, events
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pyautogui
import subprocess

API_ID = 20155181
API_HASH = "db6f5a870fb42e682bseqw8d9e4e9cec0"
TARGET_CHAT =-1002191668970 #-4859742164

SENDER_CHAT=-4859742164

YOUTUBE_URL_PATTERN = re.compile(
    r"https?://(?:www\.)?(?:youtube\.com/[^\s]+|youtu\.be/[^\s]+)",
    re.IGNORECASE
)

SESSION_NAME = "tg_youtube_opener_session"


def extract_youtube_urls(text: str):
    if not text:
        return []
    urls = YOUTUBE_URL_PATTERN.findall(text)
    return list(set(urls))


# Kill all running Chrome processes
def kill_chrome():
    try:
        subprocess.run("taskkill /F /IM chrome.exe", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("✅ All Chrome processes killed")
    except Exception as e:
        print("⚠️ Could not kill Chrome processes:", e)

async def main():
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

    @client.on(events.NewMessage(chats=TARGET_CHAT))
    async def handler(event):
        text = event.message.message or ""
        urls = extract_youtube_urls(text)

        if not urls:
            return

        for url in urls:
            print(f"[YOUTUBE LINK FOUND] {url}")

            kill_chrome()  # kill existing Chrome sessions

            # 🔑 Create driver *inside* handler, using your profile
            
            selenium_profile = os.path.expanduser(r"~\AppData\Local\Google\Chrome\SeleniumProfile")
            os.makedirs(selenium_profile, exist_ok=True)

            options = webdriver.ChromeOptions()
            options.add_argument(f"user-data-dir={selenium_profile}")
            options.add_argument("--start-maximized")

            driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=options
            )

            # ✅ Navigate directly
            driver.execute_script(f"window.location.href='{url}';")

            try:
                wait = WebDriverWait(driver, 15)

                # ▶️ Play video
                play_button = wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button.ytp-play-button"))
                )
                ActionChains(driver).move_to_element(play_button).click().perform()
                print("▶️ Video started playing...")

                # 👍 Like after 5 sec
                await asyncio.sleep(5)
                like_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label*='like this video']"))
                )
                like_button.click()
                print("👍 Video liked...")

            except Exception as e:
                print("⚠️ Could not click play/like:", e)

            # Random wait
            delay = random.randint(10, 20)
            print(f"⏳ Waiting {delay} seconds before screenshot...")
            await asyncio.sleep(delay)

            screenshot_path = "screenshot.png"
            pyautogui.screenshot(screenshot_path)
            print(f"📸 Screenshot saved -> {screenshot_path}")

            await client.send_file(SENDER_CHAT, screenshot_path,
                                   caption="Screenshot after playing & liking video 👆")
            os.remove(screenshot_path)

            driver.quit()
            print("❌ Browser closed.")

    print("Starting Telegram client...")
    await client.start()
    print("Listening for YouTube links...")
    await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
