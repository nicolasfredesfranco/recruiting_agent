#!/usr/bin/env python3
"""
Test Suite for LinkedIn CV Downloader
Tests browser initialization, anti-detection, and CV download process
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from linkedin_cv_downloader import LinkedInCVDownloader, HumanBehavior, BrowserController
from linkedin_cv_downloader.config import SELECTORS, TIMING
import time


class TestRunner:
    """Test runner for the CV downloader"""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.tests = []
    
    def test(self, name, func):
        """Run a test"""
        print(f"\n{'=' * 70}")
        print(f"🧪 TEST: {name}")
        print(f"{'=' * 70}\n")
        
        try:
            result = func()
            if result:
                print(f"\n✅ PASSED: {name}\n")
                self.passed += 1
            else:
                print(f"\n❌ FAILED: {name}\n")
                self.failed += 1
            self.tests.append((name, result))
            return result
        except Exception as e:
            print(f"\n❌ ERROR in {name}: {e}\n")
            import traceback
            traceback.print_exc()
            self.failed += 1
            self.tests.append((name, False))
            return False
    
    def summary(self):
        """Print test summary"""
        print(f"\n{'=' * 70}")
        print("📊 TEST SUMMARY")
        print(f"{'=' * 70}")
        print(f"✅ Passed: {self.passed}")
        print(f"❌ Failed: {self.failed}")
        print(f"📋 Total: {self.passed + self.failed}")
        print(f"{'=' * 70}\n")
        
        if self.tests:
            print("Detailed Results:")
            for name, result in self.tests:
                status = "✅" if result else "❌"
                print(f"  {status} {name}")
        print()


def test_browser_initialization():
    """Test 1: Browser initializes with anti-detection"""
    print("Testing browser initialization...")
    
    downloader = LinkedInCVDownloader(headless=False)
    
    try:
        downloader.setup_browser()
        
        # Check that browser is initialized
        assert downloader.browser is not None, "Browser not initialized"
        assert downloader.page is not None, "Page not created"
        assert downloader.controller is not None, "Controller not created"
        
        # Test navigation
        print("  → Navigating to LinkedIn...")
        downloader.page.goto("https://www.linkedin.com")
        time.sleep(2)
        
        # Check anti-detection
        print("  → Checking anti-detection...")
        webdriver_value = downloader.page.evaluate("navigator.webdriver")
        print(f"  → navigator.webdriver = {webdriver_value}")
        
        has_chrome = downloader.page.evaluate("typeof window.chrome !== 'undefined'")
        print(f"  → window.chrome exists = {has_chrome}")
        
        downloader.close()
        
        assert webdriver_value is None or webdriver_value == False, "Webdriver not hidden"
        assert has_chrome, "Chrome object not present"
        
        return True
        
    except Exception as e:
        print(f"  Error: {e}")
        if downloader.browser:
            downloader.close()
        return False


def test_human_behavior():
    """Test 2: Human behavior simulation"""
    print("Testing human behavior simulation...")
    
    try:
        # Test delays
        print("  → Testing random delays...")
        start = time.time()
        HumanBehavior.delay(100, 200)
        elapsed = time.time() - start
        assert 0.1 <= elapsed <= 0.25, f"Delay out of range: {elapsed}"
        
        # Test typing speed
        print("  → Testing typing speed...")
        wpm = HumanBehavior.typing_speed_wpm()
        assert 50 <= wpm <= 80, f"Typing speed out of range: {wpm}"
        
        # Test scroll amount
        print("  → Testing scroll amount...")
        scroll = HumanBehavior.random_scroll_amount()
        assert 250 <= scroll <= 400, f"Scroll amount out of range: {scroll}"
        
        # Test click offset
        print("  → Testing click offset...")
        x_ratio, y_ratio = HumanBehavior.random_click_offset(100, 100)
        assert 0.3 <= x_ratio <= 0.7, f"X ratio out of range: {x_ratio}"
        assert 0.3 <= y_ratio <= 0.7, f"Y ratio out of range: {y_ratio}"
        
        return True
        
    except Exception as e:
        print(f"  Error: {e}")
        return False


def test_manual_login_and_download():
    """Test 3: Manual login and single CV download"""
    print("⚠️  This test requires manual interaction\n")
    
    downloader = LinkedInCVDownloader(headless=False)
    
    try:
        # Setup
        downloader.setup_browser()
        
        # Manual login
        downloader.wait_for_manual_login()
        
        # Ask for test profile
        print("\n" + "=" * 70)
        print("Manual Test Input Required")
        print("=" * 70)
        choice = input("\nTest with:\n  1. Name search\n  2. Direct URL\n\nChoice (1-2): ").strip()
        
        if choice == "1":
            name = input("\nEnter person name to search: ").strip()
            if not name:
                name = "Sebastian Torres"
            success = downloader.download_cv_by_name(name)
        else:
            url = input("\nEnter profile URL: ").strip()
            if not url:
                url = "https://www.linkedin.com/in/sebastian-torres-c/"
            success = downloader.download_cv_from_url(url)
        
        downloader.close()
        return success
        
    except Exception as e:
        print(f"  Error: {e}")
        if downloader.browser:
            downloader.close()
        return False


def main():
    """Run all tests"""
    
    print("\n" + "=" * 70)
    print("🧪 LINKEDIN CV DOWNLOADER - TEST SUITE")
    print("=" * 70)
    print("\nThis will run comprehensive tests of the system\n")
    print("=" * 70)
    
    runner = TestRunner()
    
    # Run tests
    runner.test("Browser Initialization & Anti-Detection", test_browser_initialization)
    runner.test("Human Behavior Simulation", test_human_behavior)
    
    # Ask if user wants to run manual test
    print("\n" + "=" * 70)
    manual = input("\nRun manual login & download test? (y/n): ").strip().lower()
    if manual == 'y':
        runner.test("Manual Login & CV Download", test_manual_login_and_download)
    
    # Summary
    runner.summary()
    
    if runner.failed == 0:
        print("🎉 All tests passed!\n")
        return 0
    else:
        print("⚠️  Some tests failed\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
