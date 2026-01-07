#!/usr/bin/env python3
"""
LinkedIn CV Downloader - Main Execution Script
Downloads CVs from LinkedIn profiles based on config.py settings

Usage:
    python main.py

Configuration:
    Edit config.py to set credentials and download criteria
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from linkedin_cv_downloader import LinkedInCVDownloader

# Import configuration
try:
    import config
except ImportError:
    print("❌ Error: config.py not found!")
    print("Please create config.py with your settings.")
    print("See config.example.py for reference.")
    sys.exit(1)


def main():
    """Main execution function"""
    
    print("\n" + "=" * 70)
    print("🤖 LinkedIn CV Downloader - Automated Execution")
    print("=" * 70)
    print(f"\nMode: {'Search by Name' if config.SEARCH_BY_NAME else 'Direct URLs'}")
    print(f"Auto-Login: {'Enabled' if config.AUTO_LOGIN else 'Disabled'}")
    print(f"Max Downloads: {config.MAX_DOWNLOADS}")
    print("=" * 70 + "\n")
    
    # Get profiles to download
    if config.SEARCH_BY_NAME:
        profiles = config.PEOPLE_TO_DOWNLOAD[:config.MAX_DOWNLOADS]
        search_mode = True
        print(f"📋 Downloading {len(profiles)} CVs by name search\n")
    else:
        profiles = config.PROFILE_URLS[:config.MAX_DOWNLOADS]
        search_mode = False
        print(f"📋 Downloading {len(profiles)} CVs from URLs\n")
    
    if not profiles:
        print("❌ No profiles configured!")
        print("Edit config.py and add profiles to download.")
        return 1
    
    # Initialize downloader
    print("🚀 Initializing...\n")
    downloader = LinkedInCVDownloader(
        headless=config.HEADLESS_MODE,
        download_dir=config.DOWNLOAD_DIR
    )
    
    try:
        # Setup browser
        downloader.setup_browser()
        
        # Login
        if config.AUTO_LOGIN:
            print("=" * 70)
            print("🔐 Logging in automatically...")
            print("=" * 70 + "\n")
            
            if not downloader.auto_login(config.LINKEDIN_EMAIL, config.LINKEDIN_PASSWORD):
                print("\n❌ Auto-login failed!")
                print("Please check your credentials in config.py")
                downloader.close()
                return 1
            
            print("✅ Logged in successfully!\n")
        else:
            # Manual login
            downloader.wait_for_manual_login()
        
        # Start downloading
        print("\n" + "=" * 70)
        print(f"🎬 STARTING BATCH DOWNLOAD")
        print("=" * 70 + "\n")
        
        # Download all CVs
        downloader.download_multiple_cvs(profiles, search_by_name=search_mode)
        
        # Keep browser open briefly for review
        if not config.HEADLESS_MODE:
            print("\n" + "=" * 70)
            print("Keeping browser open for 10 seconds...")
            print("=" * 70 + "\n")
            import time
            time.sleep(10)
        
        # Close
        downloader.close()
        
        # Final message
        print("\n" + "=" * 70)
        print("✅ EXECUTION COMPLETE")
        print("=" * 70)
        print(f"\n📁 CVs saved to: {config.DOWNLOAD_DIR}")
        print(f"📸 Debug screenshots (if any): {config.DEBUG_SCREENSHOT_DIR}")
        print("\n" + "=" * 70 + "\n")
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        if downloader.browser:
            downloader.close()
        return 1
    
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        if downloader.browser:
            downloader.close()
        return 1


if __name__ == "__main__":
    sys.exit(main())
