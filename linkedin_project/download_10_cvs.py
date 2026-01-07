#!/usr/bin/env python3
"""
Batch Download - 10 CVs Sequential
Downloads CVs from 10 different LinkedIn profiles sequentially with human-like behavior
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from linkedin_cv_downloader import LinkedInCVDownloader


def main():
    print("\n" + "=" * 70)
    print("📦 BATCH CV DOWNLOAD - 10 Profiles")
    print("=" * 70)
    print("\nThis will download CVs from 10 different people sequentially")
    print("Each download uses human-like behavior for maximum stealth")
    print("=" * 70 + "\n")
    
    # List of 10 people to search (you can modify these names)
    people_to_search = [
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
    
    print("📋 List of people to download:")
    for i, name in enumerate(people_to_search, 1):
        print(f"   {i}. {name}")
    
    print("\n" + "=" * 70)
    print("🚀 Starting automatic download process...")
    print("=" * 70 + "\n")
    
    # Initialize downloader
    print("\n" + "=" * 70)
    print("🚀 Initializing LinkedIn CV Downloader")
    print("=" * 70 + "\n")
    
    downloader = LinkedInCVDownloader(headless=False)
    
    try:
        # Setup browser
        downloader.setup_browser()
        
        # Automatic login
        print("=" * 70)
        print("🤖 LOGGING IN AUTOMATICALLY")
        print("=" * 70 + "\n")
        
        if not downloader.auto_login():
            print("\n❌ Auto-login failed. Please check credentials.")
            downloader.close()
            return 1
        
        print("✅ Logged in successfully!\n")
        
        # Start batch download automatically
        print("\n" + "=" * 70)
        print(f"🎬 STARTING BATCH DOWNLOAD - {len(people_to_search)} profiles")
        print("=" * 70)
        
        # Download all CVs
        downloader.download_multiple_cvs(people_to_search, search_by_name=True)
        
        # Keep browser open for review
        print("\n" + "=" * 70)
        print("Browser will stay open for 15 seconds for final review...")
        print("=" * 70 + "\n")
        
        import time
        time.sleep(15)
        
        # Close
        downloader.close()
        
        # Final summary
        print("\n" + "=" * 70)
        print("✅ BATCH DOWNLOAD COMPLETE")
        print("=" * 70)
        print(f"\n📁 Check downloads/cvs/ for the downloaded CVs")
        print(f"📸 Check downloads/debug/ for any error screenshots")
        print("\n" + "=" * 70 + "\n")
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Download interrupted by user")
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
