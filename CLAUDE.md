# CLAUDE.md - Projects Orchestrator

This file provides guidance to Claude Code (claude.ai/code) for managing automation across all projects in this directory.

## Purpose

This is the main orchestrator CLAUDE.md that manages:
- Cross-project accomplishment tracking
- Daily log generation for Obsidian
- Standardization of project CLAUDE.md files
- Automation scripts and workflows

## Recent Accomplishments

*Orchestrator-level accomplishments and automation improvements*

- 2025-01-21: Created orchestrator CLAUDE.md for cross-project automation
- 2025-01-21: Established architecture for parsing project accomplishments

## Managed Projects

*Auto-discovered projects with CLAUDE.md files:*
- `obsidian-automation/` - Obsidian vault automation tools
- `outfit-visualizer/` - [To be discovered]
- [Additional projects will be listed here by automation]

## Automation Commands

### Update All Project CLAUDE.md Files
Ensure all projects have the accomplishment logging section:
```bash
python obsidian-automation-scripts/update-project-claudemd.py
```

### Parse Daily Accomplishments
Extract today's accomplishments from all projects:
```bash
python obsidian-automation-scripts/parse-accomplishments.py
```

### Generate Obsidian Daily Note
Create/update today's daily note with all accomplishments:
```bash
python obsidian-automation-scripts/update-obsidian-daily.py
```

## Architecture

### Directory Structure
```
/home/jon/projects/
├── CLAUDE.md                    # This file (orchestrator)
├── obsidian-automation-scripts/ # Automation scripts
│   ├── update-project-claudemd.py
│   ├── parse-accomplishments.py
│   └── update-obsidian-daily.py
├── obsidian-automation/
│   └── CLAUDE.md
└── [other projects]/
    └── CLAUDE.md
```

### Workflow
1. **Discovery**: Scan for all subdirectories with CLAUDE.md files
2. **Standardization**: Ensure accomplishment sections exist
3. **Collection**: Parse accomplishments from all projects
4. **Integration**: Update Obsidian vault with daily summaries

## Configuration

### Obsidian Vault Path
```
OBSIDIAN_VAULT_PATH=/home/jon/obsidian-vault  # Update this to your actual vault path
```

### Daily Note Format
```
Daily Notes/YYYY/MM-MMMM/YYYY-MM-DD.md
```

## Development Guidelines

When working at this orchestrator level:
- Focus on automation and cross-project operations
- Don't modify individual project code
- Update this file with new automation capabilities
- Test scripts carefully before running across all projects
- Log all orchestrator actions in Recent Accomplishments