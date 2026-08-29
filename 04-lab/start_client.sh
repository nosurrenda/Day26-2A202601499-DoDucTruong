#!/bin/bash
# Start ADK Web UI for Weather Agent
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/mcp-client" || exit 1

if [ -f "$SCRIPT_DIR/../.venv/bin/adk" ]; then
    ADK="$SCRIPT_DIR/../.venv/bin/adk"
else
    ADK="adk"
fi

echo "🚀 Starting ADK Web UI on http://localhost:8000..."
$ADK web
