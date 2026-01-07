"""
LinkedIn CV Downloader - Main Module
Complete automation system for downloading CVs from LinkedIn
"""

from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
import time
import random

from .browser_control import BrowserController
from .human_behavior import HumanBehavior
from .config import (
    BROWSER_CONFIG, BROWSER_ARGS, ANTI_DETECTION_SCRIPT,
    SELECTORS, TIMING, DOWNLOAD_DIR, DEBUG_SCREENSHOT_DIR
)


class LinkedInCVDownloader:
    """
    Main class for downloading CVs from LinkedIn with human-like behavior
    """
    
    def __init__(self, headless=False, download_dir=None):
        """
        Initialize the downloader
        
        Args:
            headless: Run browser in headless mode (not recommended for stealth)
            download_dir: Directory to save downloads
        """
        self.headless = headless
        self.download_dir = Path(download_dir or DOWNLOAD_DIR)
        self.debug_dir = Path(DEBUG_SCREENSHOT_DIR)
        
        # Create directories
        self.download_dir.mkdir(parents=True, exist_ok=True)
        self.debug_dir.mkdir(parents=True, exist_ok=True)
        
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        self.controller = None
        
        self.stats = {
            'attempted': 0,
            'successful': 0,
            'failed': 0,
            'errors': []
        }
    
    def setup_browser(self):
        """Initialize browser with anti-detection measures"""
        print("\n🚀 Initializing browser with anti-detection...")
        
        self.playwright = sync_playwright().start()
        
        # Launch browser
        config = BROWSER_CONFIG.copy()
        config['headless'] = self.headless
        
        self.browser = self.playwright.chromium.launch(
            headless=config['headless'],
            args=BROWSER_ARGS
        )
        
        # Create context
        self.context = self.browser.new_context(
            user_agent=config['user_agent'],
            viewport=config['viewport'],
            locale=config['locale'],
            timezone_id=config['timezone'],
            accept_downloads=True
        )
        
        # Add anti-detection script
        self.context.add_init_script(ANTI_DETECTION_SCRIPT)
        
        # Create page
        self.page = self.context.new_page()
        
        # Initialize controller
        self.controller = BrowserController(self.page)
        
        print("✅ Browser initialized\n")
    
    def auto_login(self, email=None, password=None):
        """
        Automatic login to LinkedIn with human-like behavior
        
        Args:
            email: LinkedIn email (if None, uses credentials from config)
            password: LinkedIn password (if None, uses credentials from config)
        
        Returns:
            True if login successful, False otherwise
        """
        try:
            # Import credentials if not provided
            if email is None or password is None:
                try:
                    from .credentials import LINKEDIN_EMAIL, LINKEDIN_PASSWORD
                    email = email or LINKEDIN_EMAIL
                    password = password or LINKEDIN_PASSWORD
                except ImportError:
                    print("❌ Credentials not found. Please provide email and password.")
                    return False
            
            print("=" * 70)
            print("🔐 AUTOMATIC LOGIN")
            print("=" * 70)
            print("Logging in to LinkedIn automatically with human-like behavior...")
            print("=" * 70 + "\n")
            
            # Navigate to LinkedIn
            print("1️⃣ Navigating to LinkedIn...")
            self.page.goto("https://www.linkedin.com/login", wait_until="domcontentloaded")
            HumanBehavior.delay(2000, 3000)
            
            # Find email input
            print("2️⃣ Finding login form...")
            email_selectors = [
                'input[id="username"]',
                'input[name="session_key"]',
                'input[type="email"]',
                'input[autocomplete="username"]'
            ]
            
            email_input = self.controller.find_element(email_selectors, timeout=10000)
            if not email_input:
                print("   ❌ Email input not found")
                return False
            
            # Click email input
            print("3️⃣ Entering email...")
            self.controller.click_element(email_input)
            HumanBehavior.delay(300, 600)
            
            # Type email with human-like behavior
            self.controller.type_like_human(email)
            HumanBehavior.delay(500, 1000)
            
            # Find password input
            password_selectors = [
                'input[id="password"]',
                'input[name="session_password"]',
                'input[type="password"]',
                'input[autocomplete="current-password"]'
            ]
            
            password_input = self.controller.find_element(password_selectors)
            if not password_input:
                print("   ❌ Password input not found")
                return False
            
            # Click password input
            print("4️⃣ Entering password...")
            self.controller.click_element(password_input)
            HumanBehavior.delay(300, 600)
            
            # Type password with human-like behavior
            self.controller.type_like_human(password)
            HumanBehavior.delay(800, 1500)
            
            # Find and click login button
            print("5️⃣ Clicking login button...")
            login_button_selectors = [
                'button[type="submit"]',
                'button[aria-label="Sign in"]',
                'button:has-text("Sign in")',
                'button:has-text("Iniciar sesión")'
            ]
            
            login_button = self.controller.find_element(login_button_selectors)
            if not login_button:
                print("   ❌ Login button not found")
                return False
            
            self.controller.click_element(login_button)
            
            # Wait for navigation
            print("6️⃣ Waiting for login to complete...")
            HumanBehavior.delay(3000, 5000)
            
            # Check if login was successful
            try:
                # Wait for feed to load or profile indicator
                self.page.wait_for_selector(
                    'nav[aria-label="Primary Navigation"], .global-nav, .feed-identity-module',
                    timeout=15000
                )
                print("   ✓ Login successful!\n")
                
                # Additional wait to ensure everything loads
                HumanBehavior.delay(2000, 3000)
                
                return True
                
            except:
                # Check if there's a verification challenge
                current_url = self.page.url
                if 'checkpoint' in current_url or 'challenge' in current_url:
                    print("   ⚠️  Security verification required")
                    print("   Please complete the verification in the browser")
                    input("\n   Press ENTER when verification is complete...\n")
                    HumanBehavior.delay(2000, 3000)
                    return True
                else:
                    print("   ❌ Login failed - could not verify login")
                    return False
                    
        except Exception as e:
            print(f"   ❌ Auto-login error: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def wait_for_manual_login(self):
        """Wait for user to login manually"""
        print("=" * 70)
        print("🔐 MANUAL LOGIN REQUIRED")
        print("=" * 70)
        print("Please:")
        print("  1. Login to LinkedIn in the browser")
        print("  2. Complete any security verification")
        print("  3. Make sure you see your LinkedIn feed")
        print("=" * 70 + "\n")
        
        self.page.goto("https://www.linkedin.com", wait_until="domcontentloaded")
        HumanBehavior.delay(2000, 3000)
        
        input("✋ Press ENTER when logged in and ready...\n")
        
        # Verify login
        try:
            self.page.wait_for_selector(SELECTORS['navigation'], timeout=5000)
            print("✅ Login verified\n")
            return True
        except:
            print("⚠️  Could not verify login, continuing anyway...\n")
            return True
    
    def download_cv_by_name(self, person_name, max_retries=3):
        """
        Search for a person and download their CV
        
        Args:
            person_name: Name of the person to search
            max_retries: Maximum number of retries on failure
        
        Returns:
            True if successful, False otherwise
        """
        print(f"\n{'=' * 70}")
        print(f"📄 Downloading CV: {person_name}")
        print(f"{'=' * 70}\n")
        
        self.stats['attempted'] += 1
        
        for attempt in range(1, max_retries + 1):
            try:
                if attempt > 1:
                    print(f"\n🔄 Retry attempt {attempt}/{max_retries}\n")
                
                # Step 1: Search for person
                print("1️⃣ Searching for person...")
                if not self.controller.search_person(person_name):
                    if attempt < max_retries:
                        HumanBehavior.delay(3000, 5000)
                        continue
                    print("   ❌ Search failed\n")
                    self.stats['failed'] += 1
                    self.stats['errors'].append(f"{person_name}: Search failed")
                    return False
                
                print("   ✓ Search completed\n")
                
                # Step 2: Click first result
                print("2️⃣ Opening profile...")
                if not self.controller.click_first_person_result():
                    if attempt < max_retries:
                        HumanBehavior.delay(3000, 5000)
                        continue
                    print("   ❌ Could not open profile\n")
                    self.stats['failed'] += 1
                    self.stats['errors'].append(f"{person_name}: Could not open profile")
                    return False
                
                print("   ✓ Profile opened\n")
                
                # Step 3: Download CV
                print("3️⃣ Downloading CV...")
                if not self.controller.download_cv_from_current_profile():
                    if attempt < max_retries:
                        HumanBehavior.delay(3000, 5000)
                        continue
                    print("   ❌ Download failed\n")
                    self.stats['failed'] += 1
                    self.stats['errors'].append(f"{person_name}: Download failed")
                    # Take debug screenshot
                    try:
                        screenshot_path = self.debug_dir / f"error_{person_name.replace(' ', '_')}.png"
                        self.page.screenshot(path=str(screenshot_path))
                        print(f"   📸 Debug screenshot: {screenshot_path}")
                    except:
                        pass
                    return False
                
                print(f"\n✅ CV downloaded successfully: {person_name}\n")
                self.stats['successful'] += 1
                return True
                
            except Exception as e:
                print(f"\n❌ Error (attempt {attempt}/{max_retries}): {e}\n")
                if attempt < max_retries:
                    HumanBehavior.delay(3000, 5000)
                else:
                    self.stats['failed'] += 1
                    self.stats['errors'].append(f"{person_name}: {str(e)}")
                    return False
        
        return False
    
    def download_cv_from_url(self, profile_url, person_name=None, max_retries=3):
        """
        Download CV from a direct profile URL
        
        Args:
            profile_url: URL of the LinkedIn profile
            person_name: Name for logging (optional)
            max_retries: Maximum retries
        
        Returns:
            True if successful, False otherwise
        """
        if not person_name:
            person_name = profile_url.split('/in/')[-1].rstrip('/')
        
        print(f"\n{'=' * 70}")
        print(f"📄 Downloading CV: {person_name}")
        print(f"{'=' * 70}")
        print(f"🔗 {profile_url}\n")
        
        self.stats['attempted'] += 1
        
        for attempt in range(1, max_retries + 1):
            try:
                if attempt > 1:
                    print(f"\n🔄 Retry {attempt}/{max_retries}\n")
                
                # Navigate to profile
                print("1️⃣ Navigating to profile...")
                self.page.goto(profile_url, wait_until="domcontentloaded")
                HumanBehavior.delay(*TIMING['page_load'])
                
                # Check for login wall
                if 'authwall' in self.page.url or 'login' in self.page.url:
                    print("   ❌ Login wall detected\n")
                    self.stats['failed'] += 1
                    self.stats['errors'].append(f"{person_name}: Login wall")
                    return False
                
                print("   ✓ Profile loaded\n")
                
                # Download CV
                print("2️⃣ Downloading CV...")
                if not self.controller.download_cv_from_current_profile():
                    if attempt < max_retries:
                        HumanBehavior.delay(3000, 5000)
                        continue
                    print("   ❌ Download failed\n")
                    self.stats['failed'] += 1
                    self.stats['errors'].append(f"{person_name}: Download failed")
                    return False
                
                print(f"\n✅ CV downloaded: {person_name}\n")
                self.stats['successful'] += 1
                return True
                
            except Exception as e:
                print(f"\n❌ Error (attempt {attempt}/{max_retries}): {e}\n")
                if attempt < max_retries:
                    HumanBehavior.delay(3000, 5000)
                else:
                    self.stats['failed'] += 1
                    self.stats['errors'].append(f"{person_name}: {str(e)}")
                    return False
        
        return False
    
    def download_multiple_cvs(self, profiles, search_by_name=True):
        """
        Download CVs from multiple profiles
        
        Args:
            profiles: List of names (if search_by_name) or URLs/tuples (url, name)
            search_by_name: If True, treat profiles as names to search
        """
        total = len(profiles)
        print(f"\n{'=' * 70}")
        print(f"📦 PROCESSING {total} PROFILES")
        print(f"{'=' * 70}\n")
        
        for i, profile_info in enumerate(profiles, 1):
            print(f"\n[{i}/{total}]")
            
            if search_by_name:
                # Treat as name to search
                name = profile_info
                self.download_cv_by_name(name)
            else:
                # Treat as URL or (url, name) tuple
                if isinstance(profile_info, tuple):
                    url, name = profile_info
                else:
                    url = profile_info
                    name = None
                self.download_cv_from_url(url, name)
            
            # Delay between profiles (anti-detection)
            if i < total:
                delay = random.uniform(*TIMING['between_profiles']) / 1000
                print(f"\n⏳ Waiting {delay:.1f}s before next profile...")
                time.sleep(delay)
        
        # Print summary
        self.print_summary()
    
    def print_summary(self):
        """Print download statistics"""
        print(f"\n{'=' * 70}")
        print("📊 DOWNLOAD SUMMARY")
        print(f"{'=' * 70}")
        print(f"✅ Successful: {self.stats['successful']}/{self.stats['attempted']}")
        print(f"❌ Failed: {self.stats['failed']}/{self.stats['attempted']}")
        
        if self.stats['errors']:
            print(f"\n⚠️  Errors:")
            for error in self.stats['errors'][:10]:  # Show first 10
                print(f"   • {error}")
            if len(self.stats['errors']) > 10:
                print(f"   ... and {len(self.stats['errors']) - 10} more")
        
        print(f"\n📁 Downloads saved to: {self.download_dir.absolute()}")
        print(f"{'=' * 70}\n")
    
    def close(self):
        """Close browser and cleanup"""
        if self.browser:
            print("\n🔒 Closing browser...")
            self.browser.close()
            self.playwright.stop()
            print("✅ Closed\n")
