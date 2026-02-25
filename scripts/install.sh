#!/bin/bash
# Install Mission Control CLI

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="/usr/local/bin"

echo "🦞 Installing OpenClaw Mission Control..."

# Check if we can write to /usr/local/bin
if [ ! -w "$INSTALL_DIR" ]; then
    echo "❌ Need sudo access to install to $INSTALL_DIR"
    echo "Run: sudo $0"
    exit 1
fi

# Create symlink
ln -sf "$SCRIPT_DIR/mc" "$INSTALL_DIR/mc"

# Verify installation
if command -v mc &> /dev/null; then
    echo "✅ Mission Control installed!"
    echo "   Run: mc help"
else
    echo "❌ Installation failed"
    exit 1
fi
