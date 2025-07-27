#!/usr/bin/env python3
"""
Parse accomplishments from all project CLAUDE.md files.
Extracts entries for a specific date (default: today).
"""

import os
import re
from pathlib import Path
from datetime import datetime, date
from collections import defaultdict
import json

def find_claude_md_files(root_dir=None):
    """Find all CLAUDE.md files in subdirectories."""
    if root_dir is None:
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

def parse_accomplishments(file_path, target_date=None):
    """Extract accomplishments for a specific date from CLAUDE.md."""
    if target_date is None:
        target_date = date.today()
    
    accomplishments = []
    project_name = file_path.parent.name
    
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Find the Recent Accomplishments section
        match = re.search(r'## Recent Accomplishments\s*\n(.*?)(?=\n##|\Z)', content, re.DOTALL)
        if not match:
            return accomplishments
        
        section_content = match.group(1)
        lines = section_content.split('\n')
        
        current_entry = None
        for line in lines:
            line = line.strip()
            if not line or line.startswith('*'):
                continue
            
            # Check for date line (various formats)
            date_patterns = [
                r'^-?\s*(\d{4}-\d{2}-\d{2}):?\s*(.+)$',  # - YYYY-MM-DD: content
                r'^-?\s*\*\*(\d{4}-\d{2}-\d{2})\*\*:?\s*(.+)$',  # - **YYYY-MM-DD**: content
            ]
            
            matched = False
            for pattern in date_patterns:
                match = re.match(pattern, line)
                if match:
                    entry_date_str = match.group(1)
                    entry_content = match.group(2).strip()
                    
                    try:
                        entry_date = datetime.strptime(entry_date_str, '%Y-%m-%d').date()
                        if entry_date == target_date:
                            current_entry = {
                                'project': project_name,
                                'date': entry_date_str,
                                'content': entry_content,
                                'details': []
                            }
                            accomplishments.append(current_entry)
                        else:
                            current_entry = None
                    except ValueError:
                        pass
                    
                    matched = True
                    break
            
            # If not a date line, might be a detail line
            if not matched and current_entry and line.startswith('-'):
                # Sub-bullet for current entry
                detail = line[1:].strip()
                if detail:
                    current_entry['details'].append(detail)
        
    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
    
    return accomplishments

def format_accomplishments(all_accomplishments):
    """Format accomplishments for display."""
    if not all_accomplishments:
        return "No accomplishments found for today."
    
    output = []
    
    # Group by project
    by_project = defaultdict(list)
    for acc in all_accomplishments:
        by_project[acc['project']].append(acc)
    
    for project, accs in sorted(by_project.items()):
        output.append(f"\n## {project}")
        for acc in accs:
            output.append(f"- {acc['content']}")
            for detail in acc['details']:
                output.append(f"  - {detail}")
    
    return '\n'.join(output)

def save_to_json(accomplishments, output_file):
    """Save accomplishments to JSON file for other tools."""
    with open(output_file, 'w') as f:
        json.dump(accomplishments, f, indent=2, default=str)

def main():
    """Main function to parse accomplishments."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Parse accomplishments from CLAUDE.md files')
    parser.add_argument('--date', help='Date to parse (YYYY-MM-DD), default: today')
    parser.add_argument('--json', help='Output JSON file path')
    parser.add_argument('--quiet', action='store_true', help='Suppress console output')
    
    args = parser.parse_args()
    
    # Parse target date
    if args.date:
        target_date = datetime.strptime(args.date, '%Y-%m-%d').date()
    else:
        target_date = date.today()
    
    if not args.quiet:
        print(f"📅 Parsing accomplishments for {target_date}")
        print("🔍 Searching for CLAUDE.md files...")
    
    # Find and parse all files
    claude_files = find_claude_md_files()
    all_accomplishments = []
    
    for file_path in claude_files:
        accomplishments = parse_accomplishments(file_path, target_date)
        all_accomplishments.extend(accomplishments)
        if not args.quiet and accomplishments:
            print(f"  ✓ Found {len(accomplishments)} entries in {file_path.parent.name}")
    
    # Format and display
    if not args.quiet:
        print("\n📋 Today's Accomplishments:")
        print(format_accomplishments(all_accomplishments))
    
    # Save to JSON if requested
    if args.json:
        save_to_json(all_accomplishments, args.json)
        if not args.quiet:
            print(f"\n💾 Saved to {args.json}")
    
    return all_accomplishments

if __name__ == "__main__":
    main()