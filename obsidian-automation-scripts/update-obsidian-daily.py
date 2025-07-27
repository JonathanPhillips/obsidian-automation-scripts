#!/usr/bin/env python3
"""
Update Obsidian daily note with accomplishments from all projects.
Creates or updates the daily note with a dedicated section for development work.
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime, date
import re

# Configuration - Update this to your Obsidian vault path
OBSIDIAN_VAULT_PATH = os.environ.get('OBSIDIAN_VAULT_PATH', '/home/jon/obsidian-vault')
DAILY_NOTE_FORMAT = 'Daily Notes/{year}/{month:02d}-{month_name}/{year}-{month:02d}-{day:02d}'

def get_config():
    """Get configuration from environment or config file."""
    global OBSIDIAN_VAULT_PATH
    
    config_file = Path(__file__).parent / 'config.json'
    
    if config_file.exists():
        with open(config_file, 'r') as f:
            config = json.load(f)
            return config.get('obsidian_vault_path', OBSIDIAN_VAULT_PATH)
    
    return OBSIDIAN_VAULT_PATH

def get_daily_note_path(target_date=None):
    """Generate the daily note path for a given date."""
    if target_date is None:
        target_date = date.today()
    
    month_names = ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December']
    
    path = DAILY_NOTE_FORMAT.format(
        year=target_date.year,
        month=target_date.month,
        month_name=month_names[target_date.month - 1],
        day=target_date.day
    )
    
    vault_path = Path(get_config())
    return vault_path / f"{path}.md"

def parse_accomplishments_from_json(json_file):
    """Load accomplishments from JSON file."""
    with open(json_file, 'r') as f:
        return json.load(f)

def run_accomplishment_parser(target_date=None):
    """Run the accomplishment parser and get results."""
    script_dir = Path(__file__).parent
    parser_script = script_dir / 'parse-accomplishments.py'
    temp_json = script_dir / 'temp_accomplishments.json'
    
    cmd = [sys.executable, str(parser_script), '--json', str(temp_json), '--quiet']
    if target_date:
        cmd.extend(['--date', target_date.strftime('%Y-%m-%d')])
    
    try:
        subprocess.run(cmd, check=True)
        accomplishments = parse_accomplishments_from_json(temp_json)
        temp_json.unlink()  # Clean up temp file
        return accomplishments
    except subprocess.CalledProcessError as e:
        print(f"Error running parser: {e}")
        return []

def format_accomplishments_for_obsidian(accomplishments):
    """Format accomplishments for Obsidian markdown."""
    if not accomplishments:
        return "No development accomplishments logged today."
    
    lines = []
    
    # Group by project
    projects = {}
    for acc in accomplishments:
        project = acc['project']
        if project not in projects:
            projects[project] = []
        projects[project].append(acc)
    
    for project, accs in sorted(projects.items()):
        lines.append(f"### [[{project}]]")
        for acc in accs:
            lines.append(f"- {acc['content']}")
            for detail in acc.get('details', []):
                lines.append(f"  - {detail}")
        lines.append("")  # Empty line between projects
    
    return '\n'.join(lines).strip()

def update_daily_note(accomplishments, target_date=None):
    """Update or create the daily note with accomplishments."""
    if target_date is None:
        target_date = date.today()
    
    daily_note_path = get_daily_note_path(target_date)
    
    # Ensure directory exists
    daily_note_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Section header and content
    section_header = "## Development Work"
    section_content = format_accomplishments_for_obsidian(accomplishments)
    full_section = f"{section_header}\n\n{section_content}"
    
    if daily_note_path.exists():
        # Read existing content
        with open(daily_note_path, 'r') as f:
            content = f.read()
        
        # Check if Development Work section exists
        section_pattern = r'## Development Work\s*\n(.*?)(?=\n##|\Z)'
        match = re.search(section_pattern, content, re.DOTALL)
        
        if match:
            # Replace existing section
            new_content = content[:match.start()] + full_section + content[match.end():]
        else:
            # Add section at end
            if not content.endswith('\n'):
                content += '\n'
            new_content = content + '\n' + full_section
        
        # Write updated content
        with open(daily_note_path, 'w') as f:
            f.write(new_content)
        
        print(f"✅ Updated existing daily note: {daily_note_path}")
    else:
        # Create new daily note
        date_str = target_date.strftime('%Y-%m-%d')
        weekday = target_date.strftime('%A')
        
        template = f"""# {date_str} - {weekday}

## Daily Review

### What went well today?


### What could be improved?


### Tomorrow's priorities


{full_section}

## Meeting Notes


## Other Notes

"""
        
        with open(daily_note_path, 'w') as f:
            f.write(template)
        
        print(f"✅ Created new daily note: {daily_note_path}")

def main():
    """Main function to update Obsidian daily notes."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Update Obsidian daily note with accomplishments')
    parser.add_argument('--date', help='Date to process (YYYY-MM-DD), default: today')
    parser.add_argument('--vault', help='Obsidian vault path (overrides config)')
    
    args = parser.parse_args()
    
    # Override vault path if provided
    global OBSIDIAN_VAULT_PATH
    if args.vault:
        OBSIDIAN_VAULT_PATH = args.vault
        # Force update the global before get_config is called
        os.environ['OBSIDIAN_VAULT_PATH'] = args.vault
    
    # Parse target date
    if args.date:
        target_date = datetime.strptime(args.date, '%Y-%m-%d').date()
    else:
        target_date = date.today()
    
    print(f"📅 Processing accomplishments for {target_date}")
    print(f"📁 Obsidian vault: {get_config()}")
    
    # Check if vault exists
    vault_path = Path(get_config())
    if not vault_path.exists():
        print(f"❌ Error: Obsidian vault not found at {vault_path}")
        print("Please update OBSIDIAN_VAULT_PATH in the script or set the environment variable")
        return 1
    
    # Get accomplishments
    print("🔍 Gathering accomplishments...")
    accomplishments = run_accomplishment_parser(target_date)
    
    if accomplishments:
        print(f"  ✓ Found {len(accomplishments)} accomplishments")
    else:
        print("  ℹ️  No accomplishments found")
    
    # Update daily note
    print("📝 Updating daily note...")
    update_daily_note(accomplishments, target_date)
    
    print("\n✨ Complete!")
    return 0

if __name__ == "__main__":
    sys.exit(main())