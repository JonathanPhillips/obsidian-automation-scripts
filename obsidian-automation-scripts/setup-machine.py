#!/usr/bin/env python3
"""
Setup script for deploying Obsidian automation to a new machine.
Detects environment and configures appropriate paths.
"""

import os
import sys
import platform
import json
import datetime
from pathlib import Path

def detect_environment():
    """Detect the current environment and suggest paths."""
    system = platform.system().lower()
    
    # Check for WSL
    if system == 'linux' and 'microsoft' in platform.release().lower():
        return 'wsl'
    elif system == 'linux':
        return 'linux'
    elif system == 'darwin':
        return 'macos'
    elif system == 'windows':
        return 'windows'
    else:
        return 'unknown'

def get_default_paths(env_type):
    """Get default paths for different environments."""
    username = os.getenv('USER', os.getenv('USERNAME', 'user'))
    
    paths = {
        'wsl': {
            'projects': f'/home/{username}/projects',
            'vault': f'/mnt/c/Users/{username}/Documents/Vault 76',
            'vault_alt': f'/mnt/c/Users/{username}/Documents/Obsidian Vault'
        },
        'macos': {
            'projects': f'/Users/{username}/projects',
            'vault': f'/Users/{username}/Documents/Vault 76',
            'vault_alt': f'/Users/{username}/Documents/Obsidian Vault'
        },
        'linux': {
            'projects': f'/home/{username}/projects',
            'vault': f'/home/{username}/Documents/Obsidian Vault',
            'vault_alt': f'/home/{username}/obsidian-vault'
        },
        'windows': {
            'projects': f'C:\\Users\\{username}\\projects',
            'vault': f'C:\\Users\\{username}\\Documents\\Vault 76',
            'vault_alt': f'C:\\Users\\{username}\\Documents\\Obsidian Vault'
        }
    }
    
    return paths.get(env_type, {})

def find_vault_path(default_paths):
    """Try to find the actual vault path."""
    vault_candidates = [
        default_paths.get('vault'),
        default_paths.get('vault_alt'),
    ]
    
    for path in vault_candidates:
        if path and Path(path).exists():
            return path
    
    return None

def create_config(projects_path, vault_path, env_type):
    """Create config.json for this machine."""
    config = {
        "obsidian_vault_path": vault_path,
        "daily_note_format": "Daily Notes/{year}/{month:02d}-{month_name}/{year}-{month:02d}-{day:02d}",
        "meeting_notes_path": "Meeting Notes",
        "environment": env_type,
        "projects": {
            "current_machine": projects_path
        },
        "vault_paths": {
            env_type: vault_path
        }
    }
    
    return config

def setup_automation_directory(projects_path):
    """Create automation scripts directory and copy files."""
    automation_dir = Path(projects_path) / 'automation-scripts'
    automation_dir.mkdir(parents=True, exist_ok=True)
    
    # Get the source scripts from current location
    current_script_dir = Path(__file__).parent
    scripts_to_copy = [
        'update-project-claudemd.py',
        'parse-accomplishments.py', 
        'update-obsidian-daily.py'
    ]
    
    copied = []
    for script in scripts_to_copy:
        source = current_script_dir / script
        dest = automation_dir / script
        
        if source.exists():
            try:
                import shutil
                shutil.copy2(source, dest)
                dest.chmod(0o755)  # Make executable
                copied.append(script)
            except Exception as e:
                print(f"Warning: Could not copy {script}: {e}")
    
    return automation_dir, copied

def main():
    """Main setup function."""
    print("🚀 Obsidian Automation Setup")
    print("=" * 40)
    
    # Detect environment
    env_type = detect_environment()
    print(f"📱 Detected environment: {env_type}")
    
    # Get default paths
    default_paths = get_default_paths(env_type)
    print(f"🔍 Suggested paths:")
    print(f"  Projects: {default_paths.get('projects', 'Unknown')}")
    print(f"  Vault: {default_paths.get('vault', 'Unknown')}")
    
    # Get projects path
    suggested_projects = default_paths.get('projects', '')
    projects_input = input(f"\nProjects directory [{suggested_projects}]: ").strip()
    projects_path = projects_input if projects_input else suggested_projects
    
    if not Path(projects_path).exists():
        create = input(f"Projects directory doesn't exist. Create it? [y/N]: ").strip().lower()
        if create == 'y':
            Path(projects_path).mkdir(parents=True, exist_ok=True)
            print(f"✅ Created {projects_path}")
        else:
            print("❌ Cannot proceed without projects directory")
            return 1
    
    # Find or get vault path
    found_vault = find_vault_path(default_paths)
    if found_vault:
        print(f"✅ Found Obsidian vault: {found_vault}")
        vault_path = found_vault
    else:
        print("❌ Could not auto-detect Obsidian vault")
        suggested_vault = default_paths.get('vault', '')
        vault_input = input(f"Obsidian vault path [{suggested_vault}]: ").strip()
        vault_path = vault_input if vault_input else suggested_vault
        
        if not Path(vault_path).exists():
            print(f"⚠️  Warning: Vault path doesn't exist: {vault_path}")
            proceed = input("Continue anyway? [y/N]: ").strip().lower()
            if proceed != 'y':
                return 1
    
    # Create automation directory and copy scripts
    print(f"\n📁 Setting up automation in {projects_path}")
    automation_dir, copied_scripts = setup_automation_directory(projects_path)
    
    if copied_scripts:
        print(f"✅ Copied scripts: {', '.join(copied_scripts)}")
    else:
        print("⚠️  No scripts copied - you may need to manually copy them")
    
    # Create config
    config = create_config(projects_path, vault_path, env_type)
    config_path = automation_dir / 'config.json'
    
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"✅ Created config: {config_path}")
    
    # Create orchestrator CLAUDE.md
    claude_md_path = Path(projects_path) / 'CLAUDE.md'
    if not claude_md_path.exists():
        claude_content = f"""# CLAUDE.md - Projects Orchestrator

This file provides guidance to Claude Code (claude.ai/code) for managing automation across all projects in this directory.

## Purpose

This is the main orchestrator CLAUDE.md that manages:
- Cross-project accomplishment tracking
- Daily log generation for Obsidian
- Standardization of project CLAUDE.md files
- Automation scripts and workflows

## Recent Accomplishments

*Orchestrator-level accomplishments and automation improvements*

- {datetime.date.today().strftime('%Y-%m-%d')}: Set up Obsidian automation on {env_type} environment

## Environment Configuration

- **Environment:** {env_type}
- **Projects Directory:** {projects_path}
- **Obsidian Vault:** {vault_path}

## Daily Automation Commands

### Update All Project CLAUDE.md Files
```bash
cd {projects_path}
python3 automation-scripts/update-project-claudemd.py
```

### Parse Daily Accomplishments
```bash
cd {projects_path}
python3 automation-scripts/parse-accomplishments.py
```

### Generate Obsidian Daily Note
```bash
cd {projects_path}
python3 automation-scripts/update-obsidian-daily.py
```

## Setup Complete

The automation system is now configured for this machine. Run the daily automation command at the end of each day to update your Obsidian vault with accomplishments from all projects.
"""
        
        with open(claude_md_path, 'w') as f:
            f.write(claude_content)
        
        print(f"✅ Created orchestrator: {claude_md_path}")
    else:
        print(f"ℹ️  Orchestrator already exists: {claude_md_path}")
    
    # Final instructions
    print("\n🎉 Setup Complete!")
    print(f"📁 Automation directory: {automation_dir}")
    print(f"⚙️  Configuration: {config_path}")
    print(f"🎯 Orchestrator: {claude_md_path}")
    
    print("\n📋 Next Steps:")
    print(f"1. cd {projects_path}")
    print("2. python3 automation-scripts/update-project-claudemd.py  # Add logging to existing projects")
    print("3. python3 automation-scripts/update-obsidian-daily.py     # Test daily note creation")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())