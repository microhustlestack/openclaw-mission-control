# Mission Control Web UI

Optional browser-based dashboard for OpenClaw monitoring.

## Setup

```bash
# Start web server
mc web

# Custom port
mc web --port 9090
```

Access at `http://localhost:9090`

## Features

- Live session metrics
- Visual cost charts
- One-click model switching
- Sub-agent list with controls
- Cron job status

## WebSocket Updates

The UI auto-refreshes every 5 seconds via WebSocket connection.

## API Endpoints

- `GET /api/status` — Session status JSON
- `GET /api/cost` — Today's cost
- `POST /api/switch` — Switch model
- `GET /api/agents` — Sub-agent list
- `POST /api/kill` — Kill agent

## Customization

Edit `assets/web-ui/` to customize the interface.