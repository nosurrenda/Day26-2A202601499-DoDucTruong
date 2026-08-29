#!/bin/bash
# Start MCP Weather Server on port 8085
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/mcp-server" || exit 1

if [ -f "$SCRIPT_DIR/../.venv/bin/python" ]; then
    PYTHON="$SCRIPT_DIR/../.venv/bin/python"
else
    PYTHON="python3"
fi

echo "🚀 Starting MCP Weather Server..."
$PYTHON weather.py
