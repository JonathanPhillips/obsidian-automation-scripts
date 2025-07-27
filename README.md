# Obsidian Automation Scripts

Cross-platform automation system for tracking development accomplishments and updating Obsidian daily notes.

## Quick Start

### New Machine Setup
```bash
git clone https://github.com/yourusername/obsidian-automation-scripts.git ~/projects
cd ~/projects
python3 obsidian-automation-scripts/setup-machine.py
```

### Daily Usage
```bash
cd ~/projects
python3 obsidian-automation-scripts/update-obsidian-daily.py
```

## Features

- ✅ **Cross-platform**: Works on WSL, macOS, Windows, Linux
- ✅ **Auto-discovery**: Finds all project CLAUDE.md files
- ✅ **Smart formatting**: Creates structured Obsidian daily notes
- ✅ **Environment detection**: Configures paths automatically
- ✅ **Project linking**: Uses Obsidian [[wikilinks]] for navigation

## Architecture

- **Orchestrator CLAUDE.md**: Central control at projects root
- **Project CLAUDE.md files**: Track accomplishments per project
- **Automation scripts**: Parse and format for Obsidian
- **Daily notes**: Structured updates to your vault

## Documentation

- **[DEPLOYMENT.md](DEPLOYMENT.md)**: Detailed setup instructions
- **[CLAUDE.md](CLAUDE.md)**: Orchestrator configuration
- **Scripts**: Self-documenting with `--help` flags

## Cross-Machine Workflow

1. Work on projects (any machine)
2. Claude Code updates project CLAUDE.md files
3. Run daily automation to update Obsidian
4. Sync via git + your preferred Obsidian sync method

## Supported Environments

| Environment | Projects Path | Vault Path |
|-------------|---------------|------------|
| WSL | `/home/user/projects` | `/mnt/c/Users/user/Documents/Vault 76` |
| macOS | `/Users/user/projects` | `/Users/user/Documents/Vault 76` |
| Windows | `C:\Users\user\projects` | `C:\Users\user\Documents\Vault 76` |
| Linux | `/home/user/projects` | `/home/user/Documents/Obsidian Vault` |