# Usage Guide

## Quick Start

The simplest way to use the LinkedIn CV Downloader:

```bash
python main.py
```

This reads configuration from `config.py` and downloads all configured profiles.

## Configuration

All settings are in `config.py`. Open it and configure:

### 1. Credentials

```python
LINKEDIN_EMAIL = "your.email@example.com"
LINKEDIN_PASSWORD = "your_password"
```

### 2. Download Criteria

**Option A: Search by Name**

```python
SEARCH_BY_NAME = True

PEOPLE_TO_DOWNLOAD = [
    "Sebastian Torres",
    "Maria Rodriguez Engineer",
    "Carlos Gomez Developer"
]
```

**Option B: Direct URLs**

```python
SEARCH_BY_NAME = False

PROFILE_URLS = [
    ("https://www.linkedin.com/in/username1/", "Person Name"),
    ("https://www.linkedin.com/in/username2/", "Another Person"),
]
```

### 3. Limits

```python
MAX_DOWNLOADS = 10      # Max CVs per session
MAX_RETRIES = 3         # Retries per failed download
```

## Running the Downloader

### Method 1: Main Script (Recommended)

```bash
python main.py
```

Reads all settings from `config.py` and runs automatically.

### Method 2: Demo Script

```bash
python demo_video.py
```

Downloads only 3 CVs for testing/demonstration.

### Method 3: Custom Python Script

Create your own script:

```python
#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from linkedin_cv_downloader import LinkedInCVDownloader

# Initialize
downloader = LinkedInCVDownloader(headless=False)
downloader.setup_browser()

# Login
downloader.auto_login("your@email.com", "password")

# Download CVs
people = ["Person 1", "Person 2", "Person 3"]
downloader.download_multiple_cvs(people, search_by_name=True)

# Close
downloader.close()
```

## Understanding the Output

### During Execution

```
🚀 Initializing browser with anti-detection...
✅ Browser initialized

🔐 AUTOMATIC LOGIN
1️⃣ Navigating to LinkedIn...
2️⃣ Finding login form...
3️⃣ Entering email...
4️⃣ Entering password...
5️⃣ Clicking login button...
6️⃣ Waiting for login to complete...
   ✓ Login successful!

[1/10]
📄 Downloading CV: Sebastian Torres
1️⃣ Searching for person...
   ✓ Search completed
2️⃣ Opening profile...
   ✓ Profile opened
3️⃣ Downloading CV...
   ✓ CV downloaded

✅ CV downloaded successfully: Sebastian Torres

⏳ Waiting 10.4s before next profile...
```

### Final Summary

```
📊 DOWNLOAD SUMMARY
══════════════════════════════════════════════════════════════════════
✅ Successful: 8/10
❌ Failed: 2/10

⚠️  Errors:
   • Person XYZ: Search failed
   • Another Person: Login wall

📁 Downloads saved to: /path/to/downloads/cvs
══════════════════════════════════════════════════════════════════════
```

## Downloaded Files

CVs are saved to:
- **Location**: `downloads/cvs/`
- **Format**: PDF files
- **Naming**: `Profile_Name.pdf` or LinkedIn's default naming

Debug screenshots (on errors):
- **Location**: `downloads/debug/`
- **Format**: PNG images
- **When**: Screenshot taken on download failures

## Advanced Usage

### Headless Mode (Background)

For running in the background without visible browser:

```python
# In config.py
HEADLESS_MODE = True
```

Or programmatically:

```python
downloader = LinkedInCVDownloader(headless=True)
```

**Note**: Not recommended for first-time use. Use visible browser to verify behavior.

### Custom Timing

Adjust human-like delays in `config.py`:

```python
CUSTOM_TIMING = {
    'page_load': (2000, 3500),       # Shorter = faster, less human
    'reading': (1500, 3000),
    'between_profiles': (8000, 15000) # Longer = safer
}
```

### Search Criteria

Search with job titles or modifiers:

```python
PEOPLE_TO_DOWNLOAD = [
    "John Doe Software Engineer",
    "Jane Smith Project Manager Google",
    "Bob Johnson Data Analyst"
]
```

## Best Practices

### 1. Rate Limiting

- **Max 20-30 CVs per session**
- Wait 1-2 hours between sessions
- LinkedIn may flag excessive activity

### 2. Timing

- Use default timing values (optimized for stealth)
- Longer delays = more human-like = safer
- Don't rush downloads

### 3. Error Handling

- Check debug screenshots on failures
- Update selectors if LinkedIn UI changed
- Re-run failed downloads separately

### 4. Security

- Never commit `config.py` with real credentials
- Use environment variables for production
- Enable 2FA on LinkedIn (may need manual verification)

## Common Workflows

### Workflow 1: Download from Job Search Results

1. Search LinkedIn for candidates
2. Copy names to `config.py`
3. Run `python main.py`
4. CVs saved to `downloads/cvs/`

### Workflow 2: Download from List of URLs

1. Collect profile URLs
2. Add to `PROFILE_URLS` in `config.py`
3. Set `SEARCH_BY_NAME = False`
4. Run `python main.py`

### Workflow 3: Targeted Download

For specific profiles:

```python
# custom_download.py
from src.linkedin_cv_downloader import LinkedInCVDownloader

downloader = LinkedInCVDownloader(headless=False)
downloader.setup_browser()
downloader.auto_login("email", "password")

# Download just one
downloader.download_cv_by_name("Specific Person Name")

downloader.close()
```

## Monitoring Progress

The system provides real-time feedback:
- ✅ = Success
- ❌ = Failure
- 🔄 = Retrying
- ⏳ = Waiting

Watch the browser window to see human-like behavior in action!

## Stopping Execution

Press `Ctrl+C` to stop gracefully:

```
^C
⚠️  Interrupted by user
🔒 Closing browser...
✅ Closed
```

The browser will close and stats will be printed.

## Next Steps

- Review `documentation/TROUBLESHOOTING.md` for common issues
- See `examples/` folder for more code examples
- Check `tests/` for testing and validation
