#!/usr/bin/env python3
"""
OpenClaw Mission Control - Dashboard
Kanban-style project progress + real-time metrics
Supports light/dark themes
"""

import json
import subprocess
import sys
import os
from datetime import datetime

# Theme configurations
THEMES = {
    "dark": {
        "bg": "\033[40m",
        "fg": "\033[37m",
        "header": "\033[1;36m",  # Cyan bold
        "accent": "\033[1;32m",  # Green bold
        "warning": "\033[1;33m",  # Yellow bold
        "error": "\033[1;31m",   # Red bold
        "info": "\033[1;34m",    # Blue bold
        "muted": "\033[90m",     # Gray
        "reset": "\033[0m",
        "kanban_todo": "\033[48;5;237m\033[37m",    # Dark gray bg
        "kanban_progress": "\033[48;5;26m\033[37m", # Blue bg
        "kanban_done": "\033[48;5;28m\033[37m",     # Green bg
        "border": "\033[38;5;240m",
    },
    "light": {
        "bg": "\033[47m",
        "fg": "\033[30m",
        "header": "\033[1;34m",  # Blue bold
        "accent": "\033[1;32m",  # Green bold
        "warning": "\033[1;33m",  # Yellow bold
        "error": "\033[1;31m",   # Red bold
        "info": "\033[1;36m",    # Cyan bold
        "muted": "\033[37m",     # Light gray
        "reset": "\033[0m",
        "kanban_todo": "\033[48;5;253m\033[30m",    # Light gray bg
        "kanban_progress": "\033[48;5;75m\033[30m",  # Light blue bg
        "kanban_done": "\033[48;5;120m\033[30m",     # Light green bg
        "border": "\033[38;5;250m",
    }
}

# Project boards data - can be extended
DEFAULT_BOARD = {
    "todo": [
        "Review agent configs",
        "Update SYSTEM.md",
        "Test local models",
    ],
    "progress": [
        "Mission Control v1",
        "Cache optimization",
    ],
    "done": [
        "Install Ollama",
        "Deploy Zero-Cost Protocol",
    ]
}

def get_theme():
    """Get current theme from env or default to dark"""
    theme_name = os.environ.get("MC_THEME", "dark").lower()
    return THEMES.get(theme_name, THEMES["dark"])

def set_theme(theme_name):
    """Set theme for current session"""
    os.environ["MC_THEME"] = theme_name

def c(color_name, text, theme=None):
    """Colorize text with theme"""
    if theme is None:
        theme = get_theme()
    return f"{theme.get(color_name, '')}{text}{theme['reset']}")

def run_command(cmd):

def get_session_status():
    """Get current OpenClaw session status"""
    output = run_command("openclaw status --json 2>/dev/null || openclaw status")
    return output

def get_cost_info():
    """Get cost information"""
    output = run_command("openclaw cost today 2>/dev/null || echo 'Cost tracking unavailable'")
    return output

def get_subagents():
    """List running sub-agents"""
    output = run_command("openclaw subagents list 2>/dev/null || echo 'No subagents'")
    return output

def get_cron_jobs():
    """List cron jobs"""
    output = run_command("openclaw cron list 2>/dev/null || echo 'No cron jobs'")
    return output

def get_ollama_models():
    """List available local models"""
    output = run_command("ollama list 2>/dev/null || echo 'Ollama not running'")
    return output

def format_dashboard():
    """Format comprehensive dashboard"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print(f"🦞 OPENCLAW MISSION CONTROL")
    print(f"   {now}\n")
    
    # Session Status
    print("─" * 50)
    print("📊 SESSION STATUS")
    print("─" * 50)
    status = get_session_status()
    print(status)
    
    # Cost Info
    print("\n" + "─" * 50)
    print("💰 COST TRACKING")
    print("─" * 50)
    cost = get_cost_info()
    print(cost)
    
    # Local Models
    print("\n" + "─" * 50)
    print("🤖 LOCAL MODELS (OLLAMA)")
    print("─" * 50)
    models = get_ollama_models()
    print(models)
    
    # Sub-agents
    print("\n" + "─" * 50)
    print("👥 SUB-AGENTS")
    print("─" * 50)
    agents = get_subagents()
    print(agents)
    
    # Cron Jobs
    print("\n" + "─" * 50)
    print("⏰ CRON JOBS")
    print("─" * 50)
    cron = get_cron_jobs()
    print(cron)
    
    print("\n" + "─" * 50)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--json":
        # JSON output for programmatic use
        data = {
            "timestamp": datetime.now().isoformat(),
            "status": get_session_status(),
            "cost": get_cost_info(),
            "models": get_ollama_models(),
            "agents": get_subagents(),
            "cron": get_cron_jobs()
        }
        print(json.dumps(data, indent=2))
    else:
        format_dashboard()
