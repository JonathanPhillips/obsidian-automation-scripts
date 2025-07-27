# Obsidian Automation - Multi-Machine Deployment

## Overview

This automation system tracks accomplishments across all your development projects and automatically updates your Obsidian daily notes. It works across different operating systems and environments.

## Quick Setup for New Machines

### Method 1: Automated Setup (Recommended)

1. **Copy the automation directory** to your new machine
2. **Run the setup script:**
   ```bash
   python3 setup-machine.py
   ```
3. **Follow the prompts** - it will auto-detect your environment and suggest paths

### Method 2: Manual Setup

1. **Create projects directory structure:**
   ```bash
   mkdir -p ~/projects/obsidian-automation-scripts
   ```

2. **Copy these files to `~/projects/obsidian-automation-scripts/`:**
   - `update-project-claudemd.py`
   - `parse-accomplishments.py`
   - `update-obsidian-daily.py`
   - `setup-machine.py`

3. **Create `config.json`** with your machine-specific paths:
   ```json
   {
     "obsidian_vault_path": "/path/to/your/vault",
     "daily_note_format": "Daily Notes/{year}/{month:02d}-{month_name}/{year}-{month:02d}-{day:02d}",
     "environment": "your_env_type"
   }
   ```

4. **Create orchestrator CLAUDE.md** in your projects directory

## Environment-Specific Paths

### WSL (Windows Subsystem for Linux)
- **Projects:** `/home/username/projects`
- **Vault:** `/mnt/c/Users/username/Documents/Vault 76`

### macOS
- **Projects:** `/Users/username/projects`
- **Vault:** `/Users/username/Documents/Vault 76`

### Windows
- **Projects:** `C:\\Users\\username\\projects`
- **Vault:** `C:\\Users\\username\\Documents\\Vault 76`

### Linux
- **Projects:** `/home/username/projects`
- **Vault:** `/home/username/Documents/Obsidian Vault`

## Daily Workflow

On any machine, at the end of your work day:

```bash
cd /path/to/your/projects
python3 obsidian-automation-scripts/update-obsidian-daily.py
```

This will:
1. Scan all project CLAUDE.md files
2. Extract today's accomplishments
3. Update your Obsidian daily note

## Cross-Machine Sync

### Git-Based Sync (Recommended)
1. **Make your projects directory a git repo:**
   ```bash
   cd ~/projects
   git init
   git add automation-scripts/ CLAUDE.md
   git commit -m "Add automation system"
   git remote add origin your-repo-url
   git push -u origin main
   ```

2. **On other machines, clone and setup:**
   ```bash
   git clone your-repo-url ~/projects
   cd ~/projects
   python3 automation-scripts/setup-machine.py
   ```

### Manual Sync
- Copy the `automation-scripts/` directory
- Run setup script on each machine
- Manually sync CLAUDE.md files as needed

## Obsidian Vault Sync

Your Obsidian vault should be synced separately using:
- **Obsidian Sync** (official)
- **Git** (if vault is a repo)
- **Cloud storage** (Dropbox, iCloud, etc.)
- **Syncthing** (self-hosted)

## Troubleshooting

### Vault Not Found
```bash
# Test with explicit path
python3 automation-scripts/update-obsidian-daily.py --vault "/path/to/vault"

# Update config.json with correct path
```

### Permission Issues (Linux/macOS)
```bash
chmod +x automation-scripts/*.py
```

### WSL Path Issues
- Windows paths: `/mnt/c/Users/username/...`
- Ensure WSL can access Windows drives

### Python Not Found
- Use `python3` instead of `python`
- Install Python if needed

## Project Structure

```
~/projects/
├── CLAUDE.md                         # Orchestrator
├── obsidian-automation-scripts/      # Automation tools
│   ├── config.json                  # Machine-specific config
│   ├── update-project-claudemd.py
│   ├── parse-accomplishments.py
│   ├── update-obsidian-daily.py
│   └── setup-machine.py
├── project-1/
│   └── CLAUDE.md                    # Project accomplishments
├── project-2/
│   └── CLAUDE.md
└── ...
```

## Tips

1. **Test on each machine:** Run the automation once to verify paths
2. **Standardize vault structure:** Use same daily note format across machines
3. **Regular updates:** Run daily automation consistently
4. **Backup your config:** Keep `config.json` in version control (without sensitive paths)
5. **Environment variables:** Use `OBSIDIAN_VAULT_PATH` environment variable for flexibility

## Support

If you encounter issues:
1. Check file paths and permissions
2. Verify Obsidian vault accessibility
3. Test with `--vault` flag for path debugging
4. Ensure Python 3 is available