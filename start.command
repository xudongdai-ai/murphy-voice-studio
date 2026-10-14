#!/bin/bash
set -e

PACKAGE_DIR="$(cd "$(dirname "$0")" && pwd)"
APP_DIR="$PACKAGE_DIR/app"

if [ -n "${AI_CLONE_PYTHON:-}" ]; then
    PYTHON_BIN="$AI_CLONE_PYTHON"
elif [ -x "$APP_DIR/env/bin/python" ]; then
    PYTHON_BIN="$APP_DIR/env/bin/python"
elif [ -x "$APP_DIR/.venv/bin/python" ]; then
    PYTHON_BIN="$APP_DIR/.venv/bin/python"
elif [ -x "$PACKAGE_DIR/.venv/bin/python" ]; then
    PYTHON_BIN="$PACKAGE_DIR/.venv/bin/python"
else
    echo "Install dependencies in app/env or app/.venv following README.md."
    echo "For an existing local installation, open Murphy Voice Studio.app."
    exit 1
fi

export PYTORCH_ENABLE_MPS_FALLBACK=1
export NO_PROXY="${NO_PROXY:-},localhost,127.0.0.1"
export no_proxy="$NO_PROXY"
cd "$APP_DIR"
exec "$PYTHON_BIN" app.py --open "$@"
