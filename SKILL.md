---
name: openclaw-mission-control
description: Unified command center for OpenClaw operations. Real-time cost tracking, model management, sub-agent control, cron monitoring, and automated optimization. Use when: (1) Monitoring OpenClaw session costs and cache efficiency, (2) Managing models and switching between local/remote, (3) Spawning or killing sub-agents, (4) Managing cron jobs and scheduled tasks, (5) Analyzing usage patterns and optimizing spend.
---

# OpenClaw Mission Control

Centralized command, control, and monitoring for OpenClaw operations.

## Quick Start

```bash
# View dashboard
mc status

# Switch to free model
mc switch local

# Check all sub-agents
mc agents

# View cron jobs
mc cron

# Run optimization
mc optimize
```

## Commands

### Status Dashboard
Real-time overview of costs, models, and performance.

```bash
mc status
```

Shows:
- Current model and session cost
- Cache hit rate
- Running sub-agents
- Today's spend vs budget

### Model Management

**Switch to local model (free):**
```bash
mc switch local
mc switch llama3.2
mc switch qwen2.5
```

**Switch to remote model (paid):**
```bash
mc switch remote
mc switch kimi
mc switch gemini
```

**List available models:**
```bash
mc models
```

### Sub-Agent Control

**List all agents:**
```bash
mc agents
```

**Kill an agent:**
```bash
mc kill <agent-id>
```

**Spawn new agent:**
```bash
mc spawn <task-description>
```

### Cron Management

**List cron jobs:**
```bash
mc cron
```

**Enable/disable job:**
```bash
mc cron toggle <job-name>
```

**Run job manually:**
```bash
mc cron run <job-name>
```

### Optimization

**Analyze and optimize:**
```bash
mc optimize
```

Auto-actions:
- Identifies high-cost patterns
- Suggests model switches
- Recommends cache improvements
- Flags inefficient sub-agents

## Configuration

Create `~/.openclaw/mission-control.conf`:

```json
{
  "budget_daily": 0.25,
  "budget_monthly": 5.00,
  "cache_target": 70,
  "auto_switch": true,
  "preferred_local": "llama3.2",
  "preferred_remote": "openrouter/moonshotai/kimi-k2.5"
}
```

## Scripts

- `scripts/dashboard.py` — Real-time metrics collection
- `scripts/controller.py` — Model/agent control
- `scripts/optimizer.py` — Usage analysis and recommendations
- `scripts/web_server.py` — Optional browser UI (see references/web-ui.md)

## Web Dashboard

Optional browser interface:

```bash
mc web
# Opens http://localhost:9090
```

See [references/web-ui.md] for customization.

## Automation

**Daily reports:**
```bash
mc report daily
```

**Auto-optimize on threshold:**
```bash
mc optimize --auto --threshold 0.10
```