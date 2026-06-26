#!/bin/bash
# RALPH LOOP - Autonomous Feature Implementation
# Usage: ./ralph.sh [max_iterations]
# Example: ./ralph.sh 50

set -e

MAX_ITERATIONS=${1:-20}
RALPH_DIR=".ralph"
LOG_FILE="$RALPH_DIR/ralph-loop.log"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo -e "${BLUE}[$timestamp]${NC} $1" | tee -a "$LOG_FILE"
}

log_success() {
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo -e "${GREEN}[$timestamp] ✓ $1${NC}" | tee -a "$LOG_FILE"
}

log_error() {
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo -e "${RED}[$timestamp] ✗ $1${NC}" | tee -a "$LOG_FILE"
}

echo ""
echo "============================================================================"
echo "                         RALPH LOOP v0.1.0-beta"
echo "============================================================================"
echo ""

# Check required files
log "Checking required files..."

for file in "$RALPH_DIR/PRD-ralph.md" "$RALPH_DIR/prompt.md" "$RALPH_DIR/activity.md"; do
    if [[ ! -f "$file" ]]; then
        log_error "Missing required file: $file"
        exit 1
    fi
    log_success "Found: $file"
done

echo ""
log "Starting Ralph Loop in 3 seconds..."
log "Max iterations: $MAX_ITERATIONS"
sleep 3

# Main loop
for ((i=1; i<=MAX_ITERATIONS; i++)); do
    echo ""
    echo "============================================================================"
    log "LOOP $i / $MAX_ITERATIONS"
    echo "============================================================================"

    log "Executing Claude Code..."
    output=$(claude --print "Read .ralph/prompt.md and follow the instructions. This is loop $i." 2>&1) || true

    if echo "$output" | grep -qi "promise complete"; then
        echo ""
        log_success "ALL FEATURES COMPLETED!"
        log "Total loops: $i"
        exit 0
    fi

    log "Loop $i completed. Continuing..."
    sleep 2
done

echo ""
log_error "MAX ITERATIONS REACHED ($MAX_ITERATIONS)"
log "Check activity.md for progress."
exit 1
