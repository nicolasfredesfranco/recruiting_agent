#!/usr/bin/env python3
"""
LinkedIn CV Scraper - Main Entry Point

This script allows you to download CVs from LinkedIn profiles as PDFs.
"""

import sys
from pathlib import Path
from scraper import LinkedInScraper
from scraper.utils import validate_linkedin_url, get_logger

logger = get_logger(__name__)


def print_banner():
    """Print welcome banner"""
    print("\n" + "="*60)
    print("🔍 LinkedIn CV Scraper")
    print("="*60)
    print("Download LinkedIn profiles as PDF CVs")
    print("⚠️  Use responsibly and in compliance with LinkedIn ToS")
    print("="*60 + "\n")


def get_profile_urls() -> list[str]:
    """
    Get profile URLs from user input
    
    Returns:
        List of valid LinkedIn profile URLs
    """
    print("Enter LinkedIn profile URLs (one per line).")
    print("Press Enter twice when done, or 'q' to quit:\n")
    
    urls = []
    while True:
        try:
            url = input(f"Profile #{len(urls) + 1}: ").strip()
            
            if url.lower() == 'q':
                print("\nExiting...\n")
                sys.exit(0)
            
            if not url:
                if urls:
                    break
                else:
                    print("Please enter at least one URL.\n")
                    continue
            
            if validate_linkedin_url(url):
                urls.append(url)
                print(f"✅ Added: {url}\n")
            else:
                print(f"❌ Invalid LinkedIn URL. Please use format: https://www.linkedin.com/in/username/\n")
                
        except KeyboardInterrupt:
            print("\n\nExiting...\n")
            sys.exit(0)
    
    return urls


def main():
    """Main execution function"""
    print_banner()
    
    # Create downloads directory if it doesn't exist
    downloads_dir = Path("downloads")
    downloads_dir.mkdir(exist_ok=True)
    
    # Get profile URLs from user
    profile_urls = get_profile_urls()
    
    if not profile_urls:
        print("No URLs provided. Exiting.\n")
        return
    
    print(f"\n📋 Will download {len(profile_urls)} profile(s)\n")
    
    # Initialize scraper
    try:
        with LinkedInScraper(download_path="downloads", headless=False) as scraper:
            # Manual login
            print("Step 1: Login to LinkedIn\n")
            if not scraper.login_manual(wait_time=120):
                print("❌ Login failed or timed out. Please try again.\n")
                return
            
            # Download CVs
            print("Step 2: Downloading CVs\n")
            
            if len(profile_urls) == 1:
                # Single download
                result = scraper.download_cv_as_pdf(profile_urls[0])
                if result:
                    print(f"\n✅ Success! CV saved to: {result}\n")
                else:
                    print(f"\n❌ Failed to download CV\n")
            else:
                # Batch download
                results = scraper.batch_download(profile_urls)
                
                # Show results
                print("\n📁 Downloaded files:")
                for url, filepath in results.items():
                    if filepath:
                        print(f"  ✅ {filepath}")
                    else:
                        print(f"  ❌ {url} - FAILED")
                print()
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user. Cleaning up...\n")
    except Exception as e:
        logger.error(f"Error in main: {e}")
        print(f"\n❌ An error occurred: {e}\n")
    
    print("Done! 👋\n")


if __name__ == "__main__":
    main()
