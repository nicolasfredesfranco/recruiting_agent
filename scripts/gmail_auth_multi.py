#!/usr/bin/env python3
"""
Multi-Account Gmail OAuth 2.0 Authentication Script
Supports multiple Gmail accounts with separate tokens
"""

import os
import sys
from pathlib import Path

# Add config path
CONFIG_DIR = Path(__file__).parent.parent / "config" / "gmail"
CREDENTIALS_DIR = CONFIG_DIR / "accounts"

# Gmail API scopes
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/gmail.modify'
]

# Supported accounts
ACCOUNTS = {
    'personal': {
        'email': 'nico.fredes.franco@gmail.com',
        'credentials': CREDENTIALS_DIR / 'personal_credentials.json',
        'token': CREDENTIALS_DIR / 'personal_token.json'
    },
    'jobsity': {
        'email': 'nicolas.fredes@jobsity.com',
        'credentials': CREDENTIALS_DIR / 'jobsity_credentials.json',
        'token': CREDENTIALS_DIR / 'jobsity_token.json'
    }
}

def authenticate_account(account_name, account_config):
    """Authenticate a specific account"""
    
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
    
    print(f"\n{'='*60}")
    print(f"Authenticating: {account_config['email']}")
    print(f"{'='*60}\n")
    
    credentials_file = account_config['credentials']
    token_file = account_config['token']
    
    # Check if credentials.json exists
    if not credentials_file.exists():
        print(f"❌ Error: credentials file not found")
        print(f"Expected location: {credentials_file}")
        print(f"\nPlease download OAuth 2.0 credentials from Google Cloud Console")
        print(f"and save as: {credentials_file.name}")
        return False
    
    creds = None
    
    # Load existing token
    if token_file.exists():
        print("📄 Loading existing token...")
        creds = Credentials.from_authorized_user_file(str(token_file), SCOPES)
    
    # Refresh or create new token
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("🔄 Refreshing expired token...")
            creds.refresh(Request())
        else:
            print("🌐 Opening browser for authorization...")
            print(f"Please authorize access for: {account_config['email']}")
            flow = InstalledAppFlow.from_client_secrets_file(
                str(credentials_file), SCOPES
            )
            creds = flow.run_local_server(port=0)
        
        # Save token
        print(f"💾 Saving token to: {token_file}")
        CREDENTIALS_DIR.mkdir(parents=True, exist_ok=True)
        with open(token_file, 'w') as token:
            token.write(creds.to_json())
    
    # Test connection
    print("\n🧪 Testing Gmail API connection...")
    try:
        service = build('gmail', 'v1', credentials=creds)
        results = service.users().labels().list(userId='me').execute()
        labels = results.get('labels', [])
        
        print(f"✅ Gmail API connected successfully!")
        print(f"📋 Found {len(labels)} labels")
        
        # Get profile info
        profile = service.users().getProfile(userId='me').execute()
        print(f"📧 Email: {profile['emailAddress']}")
        print(f"📊 Total messages: {profile['messagesTotal']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing Gmail API: {e}")
        return False

def main():
    """Authenticate all configured accounts"""
    
    print("\n" + "="*60)
    print("Multi-Account Gmail OAuth 2.0 Authentication")
    print("="*60)
    
    # Create credentials directory
    CREDENTIALS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Check if specific account requested
    if len(sys.argv) > 1:
        account_name = sys.argv[1]
        if account_name not in ACCOUNTS:
            print(f"❌ Unknown account: {account_name}")
            print(f"Available accounts: {', '.join(ACCOUNTS.keys())}")
            sys.exit(1)
        
        accounts_to_auth = {account_name: ACCOUNTS[account_name]}
    else:
        accounts_to_auth = ACCOUNTS
    
    # Authenticate each account
    results = {}
    for name, config in accounts_to_auth.items():
        results[name] = authenticate_account(name, config)
    
    # Summary
    print("\n" + "="*60)
    print("Authentication Summary")
    print("="*60)
    
    for name, success in results.items():
        status = "✅ Success" if success else "❌ Failed"
        print(f"{name:15s} ({ACCOUNTS[name]['email']:35s}): {status}")
    
    print("\n" + "="*60)
    print("Configuration complete!")
    print("="*60)
    
    print("\nUsage in Python scripts:")
    print("""
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# For personal account
creds_personal = Credentials.from_authorized_user_file(
    'config/gmail/accounts/personal_token.json'
)
service_personal = build('gmail', 'v1', credentials=creds_personal)

# For Jobsity account
creds_jobsity = Credentials.from_authorized_user_file(
    'config/gmail/accounts/jobsity_token.json'
)
service_jobsity = build('gmail', 'v1', credentials=creds_jobsity)
    """)
    
    print("\nTo authenticate a specific account only:")
    print("  python scripts/gmail_auth_multi.py personal")
    print("  python scripts/gmail_auth_multi.py jobsity")

if __name__ == '__main__':
    main()
