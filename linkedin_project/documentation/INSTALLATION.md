# Installation Guide

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Internet connection

## Step-by-Step Installation

### 1. Clone or Download the Project

```bash
cd /path/to/your/projects
# If using git:
git clone <repository_url> linkedin_project
cd linkedin_project

# Or if downloaded as ZIP, extract and cd into the directory
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `playwright==1.42.0` - Browser automation library

### 3. Install Playwright Browsers

```bash
playwright install chromium
```

This downloads the Chromium browser (approx. 150MB) needed for automation.

### 4. Configure

Copy and edit the configuration file:

```bash
# Edit config.py with your favorite text editor
nano config.py  # or vim, code, etc.
```

Set your credentials:

```python
LINKEDIN_EMAIL = "your.email@example.com"
LINKEDIN_PASSWORD = "your_password"
```

### 5. Test Installation

Run the automated tests to verify everything works:

```bash
python tests/test_downloader.py
```

You should see:
```
✅ PASSED: Browser Initialization & Anti-Detection
✅ PASSED: Human Behavior Simulation
🎉 All tests passed!
```

### 6. Run Your First Download

```bash
python demo_video.py
```

This will:
1. Open Chrome
2. Login automatically to LinkedIn
3. Download 3 CVs (demo profiles)
4. Save them to `downloads/cvs/`

## Troubleshooting Installation

### Error: "playwright" not found

```bash
# Make sure pip installed correctly
pip install --upgrade pip
pip install playwright==1.42.0
```

### Error: "Chromium executable not found"

```bash
# Install browser binaries
playwright install chromium --force
```

### Error: "Permission denied"

```bash
# On Linux/Mac, you may need:
chmod +x main.py demo_video.py
```

### Error: "ModuleNotFoundError: No module named 'linkedin_cv_downloader'"

Make sure you're running from the project root directory where `src/` folder is located.

## Verify Installation

Run this command to check everything is set up:

```bash
python -c "from src.linkedin_cv_downloader import LinkedInCVDownloader; print('✅ Installation successful!')"
```

## Next Steps

Once installed, see:
- `README.md` - Usage examples and documentation
- `documentation/quick_reference.md` - Quick command reference
- `demo_video.py` - Working example

## System Requirements

- **OS**: Linux, macOS, or Windows
- **RAM**: 2GB minimum (4GB recommended)
- **Disk**: 500MB for dependencies and browsers
- **Network**: Stable internet connection for LinkedIn access

## Security Note

The `config.py` file contains your LinkedIn credentials. Make sure to:
- Never commit it to version control
- Keep it secure and private
- Use a strong password
- Consider 2FA (manual verification may be needed on first login)
