## Telegram YouTube Automation

This project listens to a Telegram chat for YouTube links and automates actions.

- `ping.py`: Minimal listener. Opens detected YouTube links in your default browser. Includes a discovery mode to help you find a chat's numeric ID.
- `script.py`: Advanced automation. For each detected YouTube link it will:
  - Kill any running Chrome instances
  - Launch Chrome via Selenium with a dedicated profile
  - Open the video, click Play, click Like
  - Wait a random delay, take a screenshot
  - Send the screenshot back to a specified Telegram chat

### Requirements
- Windows 10/11
- Python 3.9+
- Google Chrome installed
- Telegram account

Python packages:
- `telethon`
- `selenium`
- `webdriver-manager`
- `pyautogui`

### Install
```powershell
cd D:\Node_js\telegramAutomation
python -m venv venv
venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install telethon selenium webdriver-manager pyautogui
```

### Configuration
Both scripts require Telegram API credentials from `my.telegram.org`.

1) Get API credentials
- Visit `https://my.telegram.org` → Log in → API Development Tools → Create App → copy `api_id` and `api_hash`.

2) Open and edit the script you want to run:
- In `ping.py` and `script.py`, set:
  - `API_ID`
  - `API_HASH`
  - `TARGET_CHAT`

3) Finding your chat ID (discovery mode)
- In `ping.py`, keep `TARGET_CHAT = None` and run it. When messages arrive in any chat you receive, the console will print that chat's numeric `id`. Use that value (e.g., `-1001234567890`) as `TARGET_CHAT` for private/supergroups.

4) Additional settings (script.py)
- `SENDER_CHAT`: Chat ID where screenshots will be sent.
- A dedicated Chrome profile is created at `%LOCALAPPDATA%\Google\Chrome\SeleniumProfile`.

### First run and login
On first run, the script will prompt you in the console to enter your phone and login code (Telethon session). A local session file named `tg_youtube_opener_session` will be created so you won’t have to log in again.

### Run
- Minimal version (open links only):
```powershell
venv\Scripts\Activate.ps1
python .\ping.py
```

- Advanced automation (play, like, screenshot, send back):
```powershell
venv\Scripts\Activate.ps1
python .\script.py
```

### What `script.py` does
1. Listens for new messages in `TARGET_CHAT`.
2. Extracts YouTube links using a robust regex.
3. For each link:
   - Kills running Chrome processes (`taskkill /F /IM chrome.exe`).
   - Starts Chrome with Selenium using a persistent profile.
   - Navigates to the video, presses Play, then clicks Like.
   - Waits 10–20 seconds, captures a full-screen PNG via `pyautogui`.
   - Sends the screenshot to `SENDER_CHAT`, then closes the browser.

### Notes and tips
- Chrome/Driver: `webdriver-manager` automatically installs a compatible ChromeDriver.
- Screen permissions: `pyautogui` requires that the session is unlocked and the display is available.
- UI changes: YouTube’s UI can change. If selectors stop working, adjust the CSS selectors in `script.py`.
- Responsible use: Automated likes/views can violate platform policies. Use for personal/testing purposes at your own risk.

### Troubleshooting
- Cannot log in: Ensure the phone number format is correct and that you enter the latest code from Telegram.
- No messages received: Verify `TARGET_CHAT` is correct. Use discovery mode in `test.py` to confirm the chat ID.
- Selenium fails to start: Ensure Chrome is installed and that your user has permissions to create the Selenium profile directory.
- Like/Play not clicked: Increase waits or verify selectors in `script.py` (`ytp-play-button`, `aria-label*='like this video'`).
- Screenshot not sent: Confirm `SENDER_CHAT` is valid and the file `screenshot.png` is created.

### Security
- Do not commit real `API_ID`, `API_HASH`, or chat IDs to a public repo. Consider using environment variables or a local config file.



### Frequently changing selectors and IDs
These values often need updates as your environment or external UIs change:

- Chat identifiers (Telethon)
  - `TARGET_CHAT` in `script.py` and `ping.py` (your minimal listener may be named `ping.py` in some setups):
    - Public groups: use the username (e.g., "@mygroup").
    - Private/supergroups: use the numeric ID (e.g., `-1001234567890`).
  - `SENDER_CHAT` in `script.py`: destination chat for screenshots.

- YouTube DOM selectors in `script.py` (Selenium)
  - Play button: `button.ytp-play-button`
  - Like button: `button[aria-label*='like this video']`
  - If clicks fail, update these selectors to match YouTube’s current DOM.

- Timing and waits in `script.py`
  - Element wait: `WebDriverWait(driver, 15)`
  - Delay before like: `await asyncio.sleep(5)`
  - Random delay before screenshot: `random.randint(10, 20)`

- Chrome setup in `script.py`
  - Profile path: `%LOCALAPPDATA%\Google\Chrome\SeleniumProfile`
  - Add/remove Chrome options via `webdriver.ChromeOptions()` (e.g., headless, language, window size).

- YouTube URL detection in both scripts
  - Regex `YOUTUBE_URL_PATTERN` covers `youtube.com` and `youtu.be`.
  - Extend if you need to handle Shorts, Live, or regional domains differently.

- Filenames referenced in this README
  - Minimal listener file is `ping.py` in this repo. If your local file is named `ping.py`, use that filename in commands.

