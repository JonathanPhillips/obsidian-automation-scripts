#!/bin/bash
# Quick deployment script for copying automation to a new machine

echo "🚀 Obsidian Automation Deployment"
echo "=================================="

# Get target directory
if [ "$1" = "" ]; then
    echo "Usage: $0 <target-directory>"
    echo "Example: $0 ~/projects"
    echo "Example: $0 /Users/jon/projects"
    exit 1
fi

TARGET_DIR="$1"
AUTOMATION_DIR="$TARGET_DIR/automation-scripts"

# Create target directories
echo "📁 Creating directories..."
mkdir -p "$AUTOMATION_DIR"

# Copy automation scripts
echo "📋 Copying scripts..."
cp update-project-claudemd.py "$AUTOMATION_DIR/"
cp parse-accomplishments.py "$AUTOMATION_DIR/"
cp update-obsidian-daily.py "$AUTOMATION_DIR/"
cp setup-machine.py "$AUTOMATION_DIR/"

# Make scripts executable
chmod +x "$AUTOMATION_DIR"/*.py

# Copy documentation
cp ../DEPLOYMENT.md "$TARGET_DIR/"

# Create basic orchestrator CLAUDE.md if it doesn't exist
if [ ! -f "$TARGET_DIR/CLAUDE.md" ]; then
    echo "📝 Creating orchestrator CLAUDE.md..."
    cat > "$TARGET_DIR/CLAUDE.md" << 'EOF'
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

## Setup Instructions

Run the setup script to configure for this machine:
```bash
python3 automation-scripts/setup-machine.py
```
EOF
fi

echo "✅ Deployment complete!"
echo ""
echo "📋 Next steps:"
echo "1. cd $TARGET_DIR"
echo "2. python3 automation-scripts/setup-machine.py"
echo "3. Follow the setup prompts"
echo ""
echo "📖 For detailed instructions, see: $TARGET_DIR/DEPLOYMENT.md"