#!/usr/bin/env python3
"""
OpenClaw Mission Control - Controller
Model switching and agent management
"""

import subprocess
import sys
import json

LOCAL_MODELS = {
    "llama3.2": "local/llama3.2",
    "llama3.1": "local/llama3.1",
    "llama3": "local/llama3",
    "qwen2.5": "local/qwen2.5",
    "qwen": "local/qwen",
}

REMOTE_MODELS = {
    "kimi": "openrouter/moonshotai/kimi-k2.5",
    "gemini": "openrouter/google/gemini-2.0-flash",
}

def run_command(cmd):
    """Execute shell command"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        return result.returncode == 0, result.stdout + result.stderr
    except Exception as e:
        return False, str(e)

def switch_model(model_name):
    """Switch to specified model"""
    if model_name in LOCAL_MODELS:
        model = LOCAL_MODELS[model_name]
        print(f"🔄 Switching to local model: {model_name}")
    elif model_name in REMOTE_MODELS:
        model = REMOTE_MODELS[model_name]
        print(f"🔄 Switching to remote model: {model_name}")
    else:
        # Assume it's a full model path
        model = model_name
        print(f"🔄 Switching to: {model}")
    
    success, output = run_command(f"openclaw model set {model}")
    if success:
        print(f"✅ Switched to {model}")
    else:
        print(f"❌ Failed to switch: {output}")
    return success

def switch_local():
    """Switch to preferred local model"""
    # Check which local models are available
    success, output = run_command("ollama list")
    if "llama3.2" in output:
        return switch_model("llama3.2")
    elif "llama3.1" in output:
        return switch_model("llama3.1")
    else:
        print("❌ No local models found. Run: ollama pull llama3.2")
        return False

def switch_remote():
    """Switch to remote model (kimi default)"""
    return switch_model("kimi")

def list_models():
    """List all available models"""
    print("🤖 LOCAL MODELS (FREE):")
    for name, path in LOCAL_MODELS.items():
        print(f"  • {name:12} → {path}")
    
    print("\n🌐 REMOTE MODELS (PAID):")
    for name, path in REMOTE_MODELS.items():
        print(f"  • {name:12} → {path}")

def list_agents():
    """List all sub-agents"""
    print("👥 ACTIVE SUB-AGENTS:")
    success, output = run_command("openclaw subagents list")
    if success:
        print(output or "No active sub-agents")
    else:
        print(f"Error: {output}")

def kill_agent(agent_id):
    """Kill a sub-agent"""
    print(f"💀 Killing agent: {agent_id}")
    success, output = run_command(f"openclaw subagents kill {agent_id}")
    if success:
        print(f"✅ Agent {agent_id} terminated")
    else:
        print(f"❌ Failed to kill: {output}")
    return success

def spawn_agent(task):
    """Spawn a new sub-agent"""
    print(f"🆕 Spawning agent for: {task}")
    # Use local model by default for cost efficiency
    cmd = f'openclaw sessions_spawn "{task}" --local'
    success, output = run_command(cmd)
    if success:
        print(f"✅ Agent spawned: {output}")
    else:
        print(f"❌ Failed to spawn: {output}")
    return success

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: controller.py <command> [args]")
        print("Commands: switch, local, remote, models, agents, kill, spawn")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "switch" and len(sys.argv) > 2:
        switch_model(sys.argv[2])
    elif cmd == "local":
        switch_local()
    elif cmd == "remote":
        switch_remote()
    elif cmd == "models":
        list_models()
    elif cmd == "agents":
        list_agents()
    elif cmd == "kill" and len(sys.argv) > 2:
        kill_agent(sys.argv[2])
    elif cmd == "spawn" and len(sys.argv) > 2:
        spawn_agent(" ".join(sys.argv[2:]))
    else:
        print(f"Unknown command: {cmd}")
