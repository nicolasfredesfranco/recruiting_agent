# Gmail API Configuration

## Setup Instructions

### 1. Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Gmail API
4. Configure OAuth consent screen
5. Create OAuth 2.0 credentials

### 2. Download Credentials

- Download `credentials.json` from Google Cloud Console
- Place it in this directory: `config/gmail/credentials.json`

### 3. First-Time Authentication

Run the authentication script (will open browser):
```bash
python scripts/gmail_auth.py
```

This will:
- Open browser for Google authorization
- Generate `token.json` with access/refresh tokens
- Save to `config/gmail/token.json`

### 4. Files in This Directory

- `credentials.json` - OAuth 2.0 Client ID (from Google Cloud)
- `token.json` - Access & refresh tokens (generated after auth)
- `README.md` - This file

## Security Notes

⚠️ **IMPORTANT**: Add to `.gitignore`:
```
config/gmail/credentials.json
config/gmail/token.json
```

These files contain sensitive authentication data and should NEVER be committed to version control.

## Usage Example

```python
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Load credentials
creds = Credentials.from_authorized_user_file('config/gmail/token.json')

# Build service
service = build('gmail', 'v1', credentials=creds)

# Use Gmail API
messages = service.users().messages().list(userId='me').execute()
```
