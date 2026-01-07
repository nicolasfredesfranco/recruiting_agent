#!/usr/bin/env python3
"""
Visual Test - LinkedIn CV Downloader
Opens a browser and demonstrates human-like behavior
This is for visual verification and manual testing
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from linkedin_cv_downloader import LinkedInCVDownloader
import time


def visual_test_search():
    """
    Visual test that demonstrates:
    1. Browser opening with anti-detection
    2. Manual login
    3. Human-like search behavior
    4. Natural mouse movements
    5. CV download flow
    """
    
    print("\n" + "=" * 70)
    print("👁️  VISUAL TEST - LinkedIn CV Downloader")
    print("=" * 70)
    print("\nThis will open a browser window so you can SEE the human-like behavior\n")
    print("=" * 70 + "\n")
    
    # Initialize downloader (not headless for visual verification)
    downloader = LinkedInCVDownloader(headless=False)
    
    try:
        # Setup browser
        downloader.setup_browser()
        
        # Manual login
        downloader.wait_for_manual_login()
        
        print("=" * 70)
        print("🎬 READY FOR DEMONSTRATION")
        print("=" * 70)
        print("\nWatch the browser window carefully to observe:")
        print("  ✓ Natural mouse movements (Bezier curves)")
        print("  ✓ Human-like typing speed")
        print("  ✓ Realistic delays between actions")
        print("  ✓ Smooth scrolling")
        print("  ✓ Random click positions within elements")
        print("=" * 70 + "\n")
        
        # Ask what to test
        choice = input("Test with:\n  1. Search by name\n  2. Direct URL\n\nChoice (1-2): ").strip()
        
        if choice == "1":
            # Test search by name
            print("\n" + "=" * 70)
            name = input("Enter person name to search (default: Sebastian Torres): ").strip()
            if not name:
                name = "Sebastian Torres"
            
            print(f"\n👀 WATCH: I will search for '{name}' like a human\n")
            time.sleep(2)
            
            success = downloader.download_cv_by_name(name)
            
        else:
            # Test direct URL
            print("\n" + "=" * 70)
            url = input("Enter profile URL (default: Sebastian Torres): ").strip()
            if not url:
                url = "https://www.linkedin.com/in/sebastian-torres-c/"
            
            print(f"\n👀 WATCH: I will navigate and download CV like a human\n")
            time.sleep(2)
            
            success = downloader.download_cv_from_url(url)
        
        # Show result
        print("\n" + "=" * 70)
        if success:
            print("✅ Visual test PASSED")
        else:
            print("⚠️  Visual test completed with issues")
        print("=" * 70)
        
        # Keep browser open for inspection
        print("\n📋 The browser will stay open for 10 seconds so you can inspect...")
        time.sleep(10)
        
        # Print stats
        downloader.print_summary()
        
        # Close
        downloader.close()
        
        return success
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        if downloader.browser:
            downloader.close()
        return False
    
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        if downloader.browser:
            downloader.close()
        return False


def quick_visual_demo():
    """
    Quick demo that just shows mouse movements on LinkedIn homepage
    No login required
    """
    
    print("\n" + "=" * 70)
    print("🎯 QUICK VISUAL DEMO - Mouse Movements")
    print("=" * 70)
    print("\nThis will show natural mouse movements without requiring login\n")
    
    from linkedin_cv_downloader import LinkedInCVDownloader
    
    downloader = LinkedInCVDownloader(headless=False)
    
    try:
        downloader.setup_browser()
        
        # Navigate to LinkedIn
        print("📍 Navigating to LinkedIn...")
        downloader.page.goto("https://www.linkedin.com", wait_until="domcontentloaded")
        time.sleep(2)
        
        # Demonstrate mouse movements
        print("\n👀 WATCH the mouse movements - they use Bezier curves to look natural")
        print("   Moving mouse to various positions...\n")
        
        from linkedin_cv_downloader.browser_control import MouseController
        mouse = MouseController(downloader.page)
        
        # Move to several positions with natural curves
        positions = [
            (300, 200),
            (800, 400),
            (500, 600),
            (200, 300),
            (700, 200),
        ]
        
        for i, (x, y) in enumerate(positions, 1):
            print(f"  Move {i}/5: ({x}, {y})")
            mouse.move_to(x, y)
            time.sleep(1)
        
        print("\n✅ Demo complete - mouse movements should look natural!")
        print("   Browser will close in 5 seconds...\n")
        time.sleep(5)
        
        downloader.close()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        if downloader.browser:
            downloader.close()


def main():
    """Main menu"""
    
    print("\n" + "=" * 70)
    print("🧪 VISUAL TEST MENU")
    print("=" * 70)
    print("\nChoose a test:")
    print("  1. Quick mouse movement demo (no login)")
    print("  2. Full CV download test (requires login)")
    print("  3. Exit")
    print("=" * 70)
    
    choice = input("\nChoice (1-3): ").strip()
    
    if choice == "1":
        quick_visual_demo()
    elif choice == "2":
        visual_test_search()
    else:
        print("\n👋 Goodbye!\n")
        return 0
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
