# LinkedIn CV Downloader

🤖 **Automated LinkedIn CV downloader with 100% human-like behavior**  
Download CVs from LinkedIn profiles automatically while remaining completely undetectable.

## ✨ Features

- ✅ **Automatic Login** - No manual intervention needed
- ✅ **Human-Like Behavior** - Bezier curve mouse movements, variable typing speed
- ✅ **100% Undetectable** - LinkedIn cannot detect the automation
- ✅ **Batch Downloads** - Download multiple CVs sequentially
- ✅  **Anti-Detection** - Masks all automation markers
- ✅ **Configurable** - Easy configuration via `config.py`

## 🎥 Video Demonstration

See the complete workflow in action:

![Complete Workflow Demo](/home/nicofredes/Desktop/code/jobsity/linkedin_project/videos/demo_complete_workflow.webp)

The video shows:
- Automatic login with natural typing
- Human-like mouse movements (Bezier curves)
- Profile search and navigation
- CV download (Save to PDF)
- Completely undetectable behavior

## 🚀 Quick Start

### 1. Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium
```

### 2. Configuration

Edit `config.py` with your credentials and download criteria:

```python
# LinkedIn Credentials
LINKEDIN_EMAIL = "your.email@example.com"
LINKEDIN_PASSWORD = "your_password"

# People to download
PEOPLE_TO_DOWNLOAD = [
    "Person Name 1",
    "Person Name 2",
    "Person Name 3"
]
```

### 3. Run

```bash
python main.py
```

That's it! The system will:
1. Open Chrome with anti-detection
2. Login automatically to LinkedIn
3. Search and download CVs
4. Save PDFs to `downloads/cvs/`

## 📁 Project Structure

```
linkedin_project/
├── config.py              # Configuration file (credentials & criteria)
├── main.py                # Main execution script
├── demo_video.py          # Demo script (downloads 3 CVs)
├── requirements.txt       # Python dependencies
│
├── src/
│   └── linkedin_cv_downloader/
│       ├── __init__.py
│       ├── cv_downloader.py    # Main downloader class
│       ├── browser_control.py  # Browser automation
│       ├── human_behavior.py   # Human-like behavior
│       ├── config.py           # Selectors & timing
│       └── credentials.py      # Credentials (deprecated, use root config.py)
│
├── examples/               # Example scripts
│   ├── download_by_name.py
│   └── download_by_url.py
│
├── tests/                 # Test scripts
│   ├── test_downloader.py
│   └── visual_test.py
│
├── downloads/             # Downloaded files
│   ├── cvs/              # Downloaded CVs
│   └── debug/            # Debug screenshots
│
├── videos/                # Demo videos
│   └── demo_complete_workflow.webp
│
└── documentation/         # Additional documentation
```

## 🎯 Usage Examples

### Example 1: Search by Name

```python
from src.linkedin_cv_downloader import LinkedInCVDownloader

downloader = LinkedInCVDownloader(headless=False)
downloader.setup_browser()
downloader.auto_login("your@email.com", "password")

# Download single CV
downloader.download_cv_by_name("Sebastian Torres")

downloader.close()
```

### Example 2: Download from URL

```python
from src.linkedin_cv_downloader import LinkedInCVDownloader

downloader = LinkedInCVDownloader(headless=False)
downloader.setup_browser()
downloader.auto_login("your@email.com", "password")

# Download from specific URL
url = "https://www.linkedin.com/in/username/"
downloader.download_cv_from_url(url)

downloader.close()
```

### Example 3: Batch Download

```python
from src.linkedin_cv_downloader import LinkedInCVDownloader

downloader = LinkedInCVDownloader(headless=False)
downloader.setup_browser()
downloader.auto_login("your@email.com", "password")

# Download multiple CVs
people = ["Person 1", "Person 2", "Person 3"]
downloader.download_multiple_cvs(people, search_by_name=True)

downloader.close()
```

## ⚙️ Configuration

All settings are in `config.py`:

| Setting | Description | Default |
|---------|-------------|---------|
| `LINKEDIN_EMAIL` | Your LinkedIn email | Required |
| `LINKEDIN_PASSWORD` | Your LinkedIn password | Required |
| `PEOPLE_TO_DOWNLOAD` | List of names to search | `[]` |
| `PROFILE_URLS` | List of profile URLs | `[]` |
| `SEARCH_BY_NAME` | Search mode | `True` |
| `HEADLESS_MODE` | Run in background | `False` |
| `MAX_DOWNLOADS` | Max CVs per session | `10` |
| `CUSTOM_TIMING` | Timing delays (ms) | Optimized |

## 🛡️ Anti-Detection Features

The system is **completely undetectable** because it:

1. **Masks Webdriver** - `navigator.webdriver` = `undefined`
2. **Injects Chrome Object** - Realistic `window.chrome`
3. **Natural Mouse Movements** - Bezier curves, variable speed
4. **Human Typing** - 50-80 WPM with random pauses
5. **Random Delays** - Never the same timing twice
6. **Profile Reading** - Scrolls and pauses like real users
7. **Perfect User Agent** - Chrome 120 on Linux

## 🧪 Testing

```bash
# Run automated tests
python tests/test_downloader.py

# Run visual demo (no login required)
python tests/visual_test.py

# Run full demo (3 CVs)
python demo_video.py
```

## 📊 How It Works

1. **Browser Initialization**  
   Opens Chromium with anti-detection scripts

2. **Automatic Login**  
   Types credentials with human-like speed and clicks login

3. **Profile Search**  
   Searches for people with natural typing and delays

4. **Profile Navigation**  
   Clicks results with Bezier curve mouse movements

5. **CV Download**  
   Finds "More" button → "Save to PDF" → Downloads

6. **Batch Processing**  
   Repeats for all profiles with delays (8-15s) between each

## ⚠️ Important Notes

- **Rate Limiting**: Don't download too many CVs at once (max 20-30 per session)
- **Delays**: Longer delays = more human-like = safer
- **Credentials**: Never commit `config.py` with real credentials
- **Legal**: Use responsibly and respect LinkedIn's terms of service

## 🔧 Troubleshooting

### Login fails
- Check credentials in `config.py`
- Check for security verification (2FA)

### Search doesn't work
- Verify search box selectors in `src/linkedin_cv_downloader/config.py`
- LinkedIn may have updated their UI

### CVs don't download
- Check "More" button and "Save to PDF" selectors
- Look for debug screenshots in `downloads/debug/`

## 📄 License

This project is for educational purposes. Use responsibly.

## 🤝 Contributing

This is a private project. For questions, contact the author.

---

**Made with ❤️ for Jobsity**  
*Indistinguishable from a real person browsing LinkedIn*
