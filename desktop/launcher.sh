#!/bin/bash
set -u

APP_DIR="$HOME/pinokio/api/applio.git/app"
PYTHON_BIN="$APP_DIR/env/bin/python"
APP_URL="http://127.0.0.1:6969"
LOG_FILE="$HOME/Library/Logs/Murphy-Voice-Studio.log"
export PATH="$HOME/pinokio/bin/miniconda/bin:/opt/homebrew/bin:$PATH"
export PYTORCH_ENABLE_MPS_FALLBACK=1
export NO_PROXY="${NO_PROXY:-},localhost,127.0.0.1"
export no_proxy="$NO_PROXY"

if /usr/bin/curl --silent --fail --max-time 2 "$APP_URL/" >/dev/null 2>&1; then
    /usr/bin/open "$APP_URL"
    exit 0
fi

if [ ! -x "$PYTHON_BIN" ] || [ ! -f "$APP_DIR/app.py" ]; then
    /usr/bin/osascript -e 'display alert "Murphy Voice Studio could not start" message "The application or Python environment was not found. See the setup instructions in README.md." as critical'
    exit 1
fi

mkdir -p "$(dirname "$LOG_FILE")"
cd "$APP_DIR" || exit 1
nohup "$PYTHON_BIN" -u app.py >"$LOG_FILE" 2>&1 &
SERVER_PID=$!

for _ in $(seq 1 60); do
    if /usr/bin/curl --silent --fail --max-time 1 "$APP_URL/" >/dev/null 2>&1; then
        /usr/bin/open "$APP_URL"
        exit 0
    fi
    if ! kill -0 "$SERVER_PID" 2>/dev/null; then
        /usr/bin/osascript -e 'display alert "Murphy Voice Studio could not start" message "The server could not start. Check ~/Library/Logs/Murphy-Voice-Studio.log." as critical'
        exit 1
    fi
    sleep 1
done

/usr/bin/osascript -e 'display alert "Murphy Voice Studio is still starting" message "Startup exceeded 60 seconds. Check ~/Library/Logs/Murphy-Voice-Studio.log and try again."'
exit 1
