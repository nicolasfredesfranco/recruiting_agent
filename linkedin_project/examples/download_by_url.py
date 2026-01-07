#!/usr/bin/env python3
"""
Example: Download CVs from direct URLs
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from linkedin_cv_downloader import LinkedInCVDownloader


def main():
    """Download CVs from URLs"""
    
    print("\n" + "=" * 70)
    print("🤖 LinkedIn CV Downloader - Direct URLs")
    print("=" * 70)
    print("\nThis will download CVs from specific LinkedIn profile URLs\n")
    print("=" * 70)
    
    # List of profile URLs
    profiles = [
        ("https://www.linkedin.com/in/sebastian-torres-c/", "Sebastian Torres"),
        # Add more profiles here: ("URL", "Name")
    ]
    
    print(f"\n📋 Profiles to download: {len(profiles)}\n")
    
    # Create downloader
    downloader = LinkedInCVDownloader(headless=False)
    
    try:
        # Setup browser
        downloader.setup_browser()
        
        # Wait for manual login
        downloader.wait_for_manual_login()
        
        # Download CVs
        downloader.download_multiple_cvs(profiles, search_by_name=False)
        
        print("\n✅ Process completed!")
        input("\nPress ENTER to close browser...\n")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        downloader.close()


if __name__ == "__main__":
    main()
