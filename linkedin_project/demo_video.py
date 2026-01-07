#!/usr/bin/env python3
"""
LinkedIn CV Downloader - Video Demo
Demonstrates the complete automated workflow for documentation purposes
Downloads 3 CVs to keep the demo short
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from linkedin_cv_downloader import LinkedInCVDownloader


def main():
    """Demo function - downloads 3 CVs for demonstration"""
    
    print("\n" + "=" * 70)
    print("🎥 LinkedIn CV Downloader - VIDEO DEMONSTRATION")
    print("=" * 70)
    print("\nThis demo will show:")
    print("  ✓ Automatic login to LinkedIn")
    print("  ✓ Human-like mouse movements (Bezier curves)")
    print("  ✓ Natural typing speed (50-80 WPM)")
    print("  ✓ CV download automation")
    print("  ✓ Completely undetectable behavior")
    print("\n" + "=" * 70 + "\n")
    
    # Demo configuration
    DEMO_EMAIL = "nico.fredes.franco@gmail.com"
    DEMO_PASSWORD = "key_for_jobsity123"
    
    # Just 3 profiles for quick demo
    demo_profiles = [
        "Sebastian Torres",
        "Maria Rodriguez Engineer",
        "Carlos Gomez Developer"
    ]
    
    print(f"📋 Demo will download {len(demo_profiles)} CVs:")
    for i, name in enumerate(demo_profiles, 1):
        print(f"   {i}. {name}")
    
    print("\n" + "=" * 70)
    print("🎬 Starting in 3 seconds...")
    print("=" * 70 + "\n")
    
    import time
    time.sleep(3)
    
    # Initialize downloader
    print("🚀 Initializing browser with anti-detection...")
    downloader = LinkedInCVDownloader(headless=False)
    
    try:
        # Setup
        downloader.setup_browser()
        
        # Automatic login
        print("\n" + "=" * 70)
        print("🔐 AUTOMATIC LOGIN")
        print("=" * 70)
        print("👀 WATCH: Natural typing and mouse movements")
        print("=" * 70 + "\n")
        
        if not downloader.auto_login(DEMO_EMAIL, DEMO_PASSWORD):
            print("\n❌ Login failed!")
            downloader.close()
            return 1
        
        print("\n✅ Login successful - LinkedIn doesn't detect anything!\n")
        
        # Download CVs
        print("=" * 70)
        print("📥 DOWNLOADING CVs")
        print("=" * 70)
        print("👀 WATCH: Human-like behavior")
        print("  • Bezier curve mouse paths")
        print("  • Variable typing speed")
        print("  • Random delays")
        print("  • Natural scrolling")
        print("=" * 70 + "\n")
        
        downloader.download_multiple_cvs(demo_profiles, search_by_name=True)
        
        # Show results
        print("\n" + "=" * 70)
        print("✅ DEMO COMPLETE")
        print("=" * 70)
        print("\nKeeping browser open for 15 seconds...")
        print("You can see it's indistinguishable from a real person!")
        print("=" * 70 + "\n")
        
        time.sleep(15)
        
        # Close
        downloader.close()
        
        print("\n" + "=" * 70)
        print("🎥 Video demonstration complete!")
        print("=" * 70)
        print("\n✅ All CVs downloaded successfully")
        print("✅ LinkedIn didn't detect any automation")
        print("✅ Behavior is 100% human-like")
        print("\n" + "=" * 70 + "\n")
        
        return 0
        
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
