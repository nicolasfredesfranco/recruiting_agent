#!/usr/bin/env python3
"""
Simple example: Download CVs by searching for people by name
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from linkedin_cv_downloader import LinkedInCVDownloader


def main():
    """Download CVs by searching for names"""
    
    print("\n" + "=" * 70)
    print("🤖 LinkedIn CV Downloader - Search by Name")
    print("=" * 70)
    print("\nThis will search for people on LinkedIn and download their CVs\n")
    print("=" * 70)
    
    # List of names to search
    names = [
        "Sebastian Torres",
        # Add more names here
    ]
    
    print(f"\n📋 Profiles to download: {len(names)}\n")
    
    # Create downloader
    downloader = LinkedInCVDownloader(headless=False)
    
    try:
        # Setup browser
        downloader.setup_browser()
        
        # Wait for manual login
        downloader.wait_for_manual_login()
        
        # Download CVs
        downloader.download_multiple_cvs(names, search_by_name=True)
        
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
