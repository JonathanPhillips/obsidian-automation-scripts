# Security Guidelines

## Personal Information Protection

This repository contains automation scripts but **excludes personal configuration data** for security.

### What's NOT included in the repo:
- ❌ `config.json` - Contains personal paths and vault locations
- ❌ Actual project directories  
- ❌ Personal usernames or paths
- ❌ Vault contents or structure

### What IS included:
- ✅ `config.json.example` - Template with placeholder paths
- ✅ Automation scripts (no personal data)
- ✅ Documentation and setup instructions

## Setup Instructions

1. **Clone the repository**
2. **Run the setup script** - it will create personal config automatically:
   ```bash
   python3 obsidian-automation-scripts/setup-machine.py
   ```
3. **The setup script will**:
   - Auto-detect your environment
   - Prompt for your actual paths
   - Create `config.json` locally (git-ignored)

## Best Practices

- **Never commit** `config.json` with real paths
- **Keep personal vault paths** in environment variables if needed
- **Use the setup script** rather than manual configuration
- **Review .gitignore** before adding new files

## Environment Variables

For CI/CD or automated deployment, you can use:
```bash
export OBSIDIAN_VAULT_PATH="/your/vault/path"
```

The scripts will respect this environment variable.