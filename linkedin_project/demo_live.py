#!/usr/bin/env python3
"""
Standalone LinkedIn CV Download Demo
This script demonstrates the complete CV download workflow with human-like behavior.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from linkedin_cv_downloader import LinkedInCVDownloader


def main():
    print("\n" + "=" * 70)
    print("🎯 LinkedIn CV Downloader - Live Demo")
    print("=" * 70)
    print("\nThis will demonstrate the complete workflow:")
    print("  1. Open browser with anti-detection")
    print("  2. Manual login to LinkedIn")
    print("  3. Search for a person (with human-like typing)")
    print("  4. Click on profile (with natural mouse movements)")
    print("  5. Download CV (with realistic delays)")
    print("=" * 70 + "\n")
    
    input("Press ENTER to start the demo...")
    
    # Initialize
    downloader = LinkedInCVDownloader(headless=False)
    
    try:
        # Setup
        downloader.setup_browser()
        
        # Login
        downloader.wait_for_manual_login()
        
        # Choose test mode
        print("\n" + "=" * 70)
        print("Choose test mode:")
        print("  1. Search by name (shows human-like typing and search)")
        print("  2. Direct URL (shows navigation and download)")
        print("=" * 70)
        
        choice = input("\nChoice (1-2): ").strip()
        
        if choice == "1":
            # Test search by name
            name = input("\nEnter name to search (default: Sebastian Torres): ").strip()
            if not name:
                name = "Sebastian Torres"
            
            print("\n" + "=" * 70)
            print(f"🎬 STARTING: Searching for '{name}'")
            print("=" * 70)
            print("\n👀 WATCH:")
            print("  • Natural typing speed (50-80 WPM)")
            print("  • Realistic pauses")
            print("  • Smooth mouse movements (Bezier curves)")
            print("  • Random delays between actions")
            print("  • Profile reading simulation (scrolling)")
            print("\n" + "=" * 70 + "\n")
            
            input("Press ENTER to begin...")
            
            success = downloader.download_cv_by_name(name)
            
        else:
            # Test direct URL
            url = input("\nEnter profile URL (default: Sebastian Torres): ").strip()
            if not url:
                url = "https://www.linkedin.com/in/sebastian-torres-c/"
            
            print("\n" + "=" * 70)
            print(f"🎬 STARTING: Downloading CV from URL")
            print("=" * 70)
            print("\n👀 WATCH:")
            print("  • Smooth mouse movements")
            print("  • Natural scrolling")
            print("  • Realistic click delays")
            print("\n" + "=" * 70 + "\n")
            
            input("Press ENTER to begin...")
            
            success = downloader.download_cv_from_url(url)
        
        # Results
        print("\n" + "=" * 70)
        if success:
            print("✅ DEMO SUCCESSFUL!")
            print("=" * 70)
            print("\nThe CV download is in the downloads/ directory")
            print("Check the mouse movements - they should look 100% human!")
        else:
            print("⚠️  DEMO COMPLETED WITH ISSUES")
            print("=" * 70)
            print("\nPlease check the debug screenshots in debug_screenshots/")
        
        print("\n" + "=" * 70)
        
        # Show stats
        downloader.print_summary()
        
        # Keep browser open
        print("Browser will stay open for 10 seconds for inspection...")
        import time
        time.sleep(10)
        
        # Close
        downloader.close()
        
        return 0 if success else 1
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted")
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
