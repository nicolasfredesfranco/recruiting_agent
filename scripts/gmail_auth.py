#!/usr/bin/env python3
"""
Gmail OAuth 2.0 Authentication Script
Creates token.json for Gmail API access
"""

import os
import sys
from pathlib import Path

# Add config path
CONFIG_DIR = Path(__file__).parent.parent / "config" / "gmail"
CREDENTIALS_FILE = CONFIG_DIR / "credentials.json"
TOKEN_FILE = CONFIG_DIR / "token.json"

# Gmail API scopes
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/gmail.modify'
]

def main():
    """Authenticate with Gmail API and save token"""
    
    try:
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from googleapiclient.discovery import build
    except ImportError:
        print("❌ Error: Required packages not installed")
        print("\nInstall dependencies:")
        print("pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client")
        sys.exit(1)
    
    # Check if credentials.json exists
    if not CREDENTIALS_FILE.exists():
        print(f"❌ Error: credentials.json not found")
        print(f"Expected location: {CREDENTIALS_FILE}")
        print("\nPlease download OAuth 2.0 credentials from Google Cloud Console")
        print("https://console.cloud.google.com/apis/credentials")
        sys.exit(1)
    
    creds = None
    
    # Load existing token
    if TOKEN_FILE.exists():
        print("📄 Loading existing token...")
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
    
    # Refresh or create new token
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("🔄 Refreshing expired token...")
            creds.refresh(Request())
        else:
            print("🌐 Opening browser for authorization...")
            print("Please authorize access in the browser window")
            flow = InstalledAppFlow.from_client_secrets_file(
                str(CREDENTIALS_FILE), SCOPES
            )
            creds = flow.run_local_server(port=0)
        
        # Save token
        print(f"💾 Saving token to: {TOKEN_FILE}")
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
    
    # Test connection
    print("\n🧪 Testing Gmail API connection...")
    try:
        service = build('gmail', 'v1', credentials=creds)
        results = service.users().labels().list(userId='me').execute()
        labels = results.get('labels', [])
        
        print(f"✅ Gmail API connected successfully!")
        print(f"📋 Found {len(labels)} labels in your Gmail account")
        print("\nSample labels:")
        for label in labels[:5]:
            print(f"  - {label['name']}")
        
        # Get profile info
        profile = service.users().getProfile(userId='me').execute()
        print(f"\n📧 Email: {profile['emailAddress']}")
        print(f"📊 Total messages: {profile['messagesTotal']}")
        
    except Exception as e:
        print(f"❌ Error testing Gmail API: {e}")
        sys.exit(1)
    
    print("\n" + "="*60)
    print("✅ Gmail OAuth 2.0 configuration complete!")
    print("="*60)
    print(f"\nToken saved to: {TOKEN_FILE}")
    print("\nYou can now use Gmail API in your Python scripts:")
    print("""
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

creds = Credentials.from_authorized_user_file('config/gmail/token.json')
service = build('gmail', 'v1', credentials=creds)
    """)

if __name__ == '__main__':
    main()
