# GitHub Configuration

## Current Setup ✅

### Global Git Configuration
```bash
user.name = nicolasfredesfranco
user.email = nicolasfredesfranco@users.noreply.github.com
credential.helper = store
```

### Authentication Method
**SSH Key Authentication** - Active and working

#### Verify Connection
```bash
ssh -T git@github.com
# Expected output: Hi nicolasfredesfranco! You've successfully authenticated...
```

## Usage

### Clone Repositories
```bash
git clone git@github.com:nicolasfredesfranco/repository-name.git
```

### Push/Pull
```bash
git push origin main
git pull origin main
```

## Personal Access Tokens (Optional)

If you need tokens for API access or CI/CD:

1. Go to: https://github.com/settings/tokens
2. Generate new token (classic)
3. Select required scopes
4. Store securely

### Using PAT for HTTPS
```bash
git remote set-url origin https://github.com/nicolasfredesfranco/repo.git
# When prompted, use PAT as password
```
