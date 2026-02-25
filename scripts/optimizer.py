#!/usr/bin/env python3
"""
OpenClaw Mission Control - Optimizer
Usage analysis and cost optimization recommendations
"""

import subprocess
import sys
import json
from datetime import datetime, timedelta

def get_session_stats():
    """Get detailed session statistics"""
    stats = {
        "timestamp": datetime.now().isoformat(),
        "recommendations": [],
        "alerts": []
    }
    
    # Check current model
    success, output = run_command("openclaw status")
    if success:
        stats["current_status"] = output
        
        # Parse cache hit rate
        if "Cache:" in output:
            # Extract cache percentage
            for line in output.split('\n'):
                if 'Cache:' in line:
                    stats["cache_info"] = line.strip()
                    # Look for low cache warning
                    if '%' in line:
                        try:
                            pct = int(line.split('%')[0].split()[-1])
                            if pct < 50:
                                stats["alerts"].append(f"Low cache hit rate: {pct}%")
                                stats["recommendations"].append("Use /continue to preserve context; avoid /new or /reset")
                        except:
                            pass
    
    # Check cost
    success, cost_output = run_command("openclaw cost today")
    if success:
        stats["today_cost"] = cost_output
    
    return stats

def run_command(cmd):
    """Execute shell command"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
        return result.returncode == 0, result.stdout + result.stderr
    except Exception as e:
        return False, str(e)

def analyze_efficiency():
    """Analyze current efficiency and generate recommendations"""
    print("🔍 ANALYZING OPENCLAW EFFICIENCY\n")
    
    stats = get_session_stats()
    
    print("─" * 50)
    print("📊 CURRENT STATE")
    print("─" * 50)
    print(stats.get("current_status", "Status unavailable"))
    
    if "cache_info" in stats:
        print(f"\n📈 {stats['cache_info']}")
    
    print("\n" + "─" * 50)
    print("💡 RECOMMENDATIONS")
    print("─" * 50)
    
    if stats["recommendations"]:
        for i, rec in enumerate(stats["recommendations"], 1):
            print(f"{i}. {rec}")
    else:
        print("✅ No immediate optimizations needed")
    
    if stats["alerts"]:
        print("\n" + "─" * 50)
        print("⚠️  ALERTS")
        print("─" * 50)
        for alert in stats["alerts"]:
            print(f"• {alert}")
    
    # General best practices
    print("\n" + "─" * 50)
    print("📚 BEST PRACTICES")
    print("─" * 50)
    print("1. Use /continue instead of /new to preserve cache")
    print("2. Start with local models, escalate only when needed")
    print("3. Batch related tasks in one session")
    print("4. Check 'openclaw status' every 10 messages")
    print("5. Target 70%+ cache hit rate")
    
    return stats

def auto_optimize(threshold=0.10):
    """Automatically apply optimizations"""
    print(f"🤖 AUTO-OPTIMIZE (threshold: ${threshold})\n")
    
    stats = get_session_stats()
    
    # Check if we should switch to local
    success, output = run_command("openclaw status")
    if success and "openrouter" in output.lower():
        print("💡 Detected remote model. Checking if local suffices...")
        
        # Simple heuristic: if context is low, suggest local
        if "Context:" in output:
            for line in output.split('\n'):
                if 'Context:' in line and '%' in line:
                    try:
                        pct = int(line.split('%')[0].split()[-1])
                        if pct < 35:
                            print(f"🔄 Context at {pct}%. Switching to local model...")
                            run_command("openclaw model set local/llama3.2")
                            return True
                    except:
                        pass
    
    print("✅ No auto-optimizations applied")
    return False

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--auto":
        threshold = float(sys.argv[2]) if len(sys.argv) > 2 else 0.10
        auto_optimize(threshold)
    elif len(sys.argv) > 1 and sys.argv[1] == "--json":
        stats = get_session_stats()
        print(json.dumps(stats, indent=2))
    else:
        analyze_efficiency()
