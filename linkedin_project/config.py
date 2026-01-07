"""
LinkedIn CV Downloader Configuration
Configure download criteria and settings
"""

from typing import List, Tuple

# ============================================================================
# LINKEDIN CREDENTIALS
# ============================================================================
# Your LinkedIn login credentials
LINKEDIN_EMAIL = "nico.fredes.franco@gmail.com"
LINKEDIN_PASSWORD = "key_for_jobsity123"

# ============================================================================
# DOWNLOAD CRITERIA
# ============================================================================

# Search criteria - List of people to search (by name)
PEOPLE_TO_DOWNLOAD = [
    "Sebastian Torres",
    "Maria Rodriguez Engineer",
    "Carlos Gomez Developer",
    "Ana Martinez Designer",
    "Juan Lopez Manager",
    "Laura Fernandez Analyst",
    "Pedro Sanchez Consultant",
    "Sofia Ramirez Specialist",
    "Diego Morales Engineer",
    "Valentina Castro Developer"
]

# Alternative: Search by direct URLs
# Format: List of (URL, Name) tuples or just URLs
PROFILE_URLS = [
    # ("https://www.linkedin.com/in/username1/", "Person Name"),
    # ("https://www.linkedin.com/in/username2/", "Another Person"),
]

# Search mode
SEARCH_BY_NAME = True  # True: use PEOPLE_TO_DOWNLOAD, False: use PROFILE_URLS

# ============================================================================
# AUTOMATION SETTINGS
# ============================================================================

# Browser settings
HEADLESS_MODE = False  # Set to True for background operation (not recommended)
AUTO_LOGIN = True      # Automatic login (uses credentials above)

# Download limits
MAX_DOWNLOADS = 10     # Maximum number of CVs to download per session
MAX_RETRIES = 3        # Number of retries per failed download

# ============================================================================
# BEHAVIOR SETTINGS (Advanced - Don't change unless needed)
# ============================================================================

# These settings control the human-like behavior simulation
# Adjust only if you know what you're doing

# Timing ranges (in milliseconds)
CUSTOM_TIMING = {
    'page_load': (2000, 3500),       # Wait after page loads
    'reading': (1500, 3000),          # Time spent "reading" profiles
    'thinking': (500, 1200),          # Pause before actions
    'click_delay': (200, 500),        # Delay before clicking
    'menu_open': (800, 1500),         # Wait for dropdown menus
    'pdf_generation': (4000, 7000),   # Wait for PDF to generate
    'between_profiles': (8000, 15000) # Delay between downloading different profiles
}

# Typing speed (Words Per Minute)
TYPING_SPEED_MIN = 50  # Slowest typing speed
TYPING_SPEED_MAX = 80  # Fastest typing speed

# Mouse movement settings
MOUSE_BEZIER_CURVE = True      # Use Bezier curves for natural movement
MOUSE_VARIABLE_SPEED = True    # Variable speed (faster middle, slower ends)
RANDOM_CLICK_OFFSET = True     # Click at random positions within elements

# ============================================================================
# OUTPUT SETTINGS
# ============================================================================

# Download directories
DOWNLOAD_DIR = "downloads/cvs"           # Where to save CVs
DEBUG_SCREENSHOT_DIR = "downloads/debug" # Screenshots on errors

# Logging
VERBOSE_OUTPUT = True  # Show detailed progress messages
PRINT_STATISTICS = True # Show download statistics at the end

# ============================================================================
# NOTES
# ============================================================================
"""
Configuration Tips:

1. CREDENTIALS:
   - Update LINKEDIN_EMAIL and LINKEDIN_PASSWORD with your credentials
   - Never commit this file with real credentials to version control

2. DOWNLOAD CRITERIA:
   - Use PEOPLE_TO_DOWNLOAD for searching by name
   - Use PROFILE_URLS for downloading from specific URLs
   - Set SEARCH_BY_NAME to choose which method to use

3. TIMING:
   - Longer delays = more human-like but slower
   - Shorter delays = faster but potentially more detectable
   - Default values are optimized for stealth

4. SAFETY:
   - Don't set MAX_DOWNLOADS too high (LinkedIn may flag you)
   - Recommended: Max 20-30 CVs per session
   - Wait 1+ hour between sessions for best results
"""
