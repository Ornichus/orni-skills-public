#!/usr/bin/env bash
# web-pdf-compile — standalone installer (macOS / Linux)
# Usage : bash install.sh

set -e
cd "$(dirname "$0")"

echo "=== web-pdf-compile installer ==="
echo

if ! command -v node >/dev/null 2>&1; then
  echo "ERROR: Node.js is not installed. Install from https://nodejs.org (>=18)."
  exit 1
fi

NODE_VERSION_MAJOR=$(node -p "parseInt(process.versions.node.split('.')[0])")
if [ "$NODE_VERSION_MAJOR" -lt 18 ]; then
  echo "ERROR: Node.js >=18 required (found $(node --version))."
  exit 1
fi

echo "Node version : $(node --version) OK"
echo

CHROME_PATHS=(
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
  "/usr/bin/google-chrome"
  "/usr/bin/chromium"
  "/usr/bin/chromium-browser"
)
CHROME_FOUND=""
for p in "${CHROME_PATHS[@]}"; do
  if [ -e "$p" ]; then
    CHROME_FOUND="$p"
    break
  fi
done

if [ -z "$CHROME_FOUND" ]; then
  echo "WARNING: Google Chrome not found in standard locations."
  echo "         Install Chrome from https://www.google.com/chrome/"
  echo "         OR set 'chrome_path' in your sources.json"
else
  echo "Chrome found : $CHROME_FOUND"
fi
echo

echo "Installing npm dependencies (~150 MB)..."
npm install

echo
echo "=== Install complete ==="
echo
echo "Next steps :"
echo "  npm run probe -- https://your-site.com/article    # find selectors"
echo "  npm run capture -- examples/smoke-test.json       # smoke test"
echo "  npm run compile -- examples/smoke-test.json       # generate PDF"
echo
echo "PDF lands at output/<config_name>/COMPILATION.pdf"
