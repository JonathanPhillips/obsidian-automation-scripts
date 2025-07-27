#!/usr/bin/env python3
"""
Update all project CLAUDE.md files to include accomplishment logging section.
Run from /home/jon/projects/ directory.
"""

import os
from pathlib import Path
from datetime import datetime

ACCOMPLISHMENT_SECTION = """## Recent Accomplishments

*Log major tasks, features, and fixes with timestamps for daily log automation*

- {date}: Added accomplishment logging framework to CLAUDE.md
"""

GUIDELINES_SECTION = """## Accomplishment Logging Guidelines

When working on this project, Claude Code should update the "Recent Accomplishments" section with:
- Date in YYYY-MM-DD format
- Brief description of what was accomplished
- File references when relevant (e.g., "Fixed bug in parser.py:45")
- Commit hashes for significant changes
- Deployment or release information
"""

def find_claude_md_files(root_dir=None):
    """Find all CLAUDE.md files in subdirectories."""
    if root_dir is None:
        # Default to parent projects directory
        root_dir = Path(__file__).parent.parent
    else:
        root_dir = Path(root_dir)
    
    claude_files = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Skip hidden directories and automation-scripts
        dirnames[:] = [d for d in dirnames if not d.startswith('.') and d != 'automation-scripts']
        
        dirpath = Path(dirpath)
        if 'CLAUDE.md' in filenames and dirpath != root_dir:
            claude_files.append(dirpath / 'CLAUDE.md')
    
    return claude_files

def has_accomplishment_section(content):
    """Check if CLAUDE.md already has accomplishment section."""
    return "## Recent Accomplishments" in content

def update_claude_md(file_path):
    """Add accomplishment section to CLAUDE.md if missing."""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        if has_accomplishment_section(content):
            print(f"✓ {file_path} already has accomplishment section")
            return False
        
        # Find where to insert (after initial description, before first ##)
        lines = content.split('\n')
        insert_index = 0
        
        # Skip header and initial description
        for i, line in enumerate(lines):
            if line.startswith('## ') and i > 3:
                insert_index = i
                break
        else:
            insert_index = len(lines)
        
        # Insert accomplishment sections
        today = datetime.now().strftime('%Y-%m-%d')
        new_content = lines[:insert_index]
        new_content.append('')
        new_content.append(ACCOMPLISHMENT_SECTION.format(date=today))
        new_content.extend(lines[insert_index:])
        
        # Add guidelines at the end if not present
        if "## Accomplishment Logging Guidelines" not in content:
            new_content.append('')
            new_content.append(GUIDELINES_SECTION)
        
        # Write updated content
        with open(file_path, 'w') as f:
            f.write('\n'.join(new_content))
        
        print(f"✅ Updated {file_path} with accomplishment section")
        return True
        
    except Exception as e:
        print(f"❌ Error updating {file_path}: {e}")
        return False

def main():
    """Main function to update all CLAUDE.md files."""
    print("🔍 Searching for CLAUDE.md files...")
    
    claude_files = find_claude_md_files()
    print(f"\nFound {len(claude_files)} CLAUDE.md files:")
    for f in claude_files:
        print(f"  - {f}")
    
    print("\n📝 Updating files...")
    updated = 0
    for file_path in claude_files:
        if update_claude_md(file_path):
            updated += 1
    
    print(f"\n✨ Complete! Updated {updated} files.")

if __name__ == "__main__":
    main()