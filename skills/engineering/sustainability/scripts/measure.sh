#!/usr/bin/env bash
# Portable CO2/weight measurement for any already-running build.
# Usage: measure.sh <url> [output-dir]
#
# Installs lighthouse on demand via npx and @tgwf/co2 via npm into a
# throwaway temp dir — no project package.json changes required. Requires
# Node >=18.20, network access to npm on first run, and a Chrome/Chromium
# executable that Lighthouse can drive headlessly.
#
# Set GREEN_HOSTING=true if the target's hosting has been verified green
# (https://www.thegreenwebfoundation.org/green-web-check/); defaults to
# false (non-green), the conservative assumption.
set -euo pipefail

# Pinned deliberately so before/after and longitudinal measurements stay
# comparable across runs. Bump these intentionally, not automatically.
LIGHTHOUSE_VERSION="12.6.0"
CO2_VERSION="0.19.0"
GREEN_HOSTING="${GREEN_HOSTING:-false}"

URL="${1:?Usage: measure.sh <url-to-a-running-build> [output-dir]}"
OUT_DIR="${2:-./sustainability-report}"
mkdir -p "$OUT_DIR"
REPORT_JSON="$(cd "$OUT_DIR" && pwd)/lighthouse.json"

echo "Auditing $URL with Lighthouse..."
npx --yes "lighthouse@$LIGHTHOUSE_VERSION" "$URL" \
  --output=json \
  --output-path="$REPORT_JSON" \
  --chrome-flags="--headless=new" \
  --only-categories=performance,seo \
  --quiet

# @tgwf/co2 is installed into its own throwaway project directory rather than
# via `npx -p`, since `npx -p` only adds the temp package's bin/ to PATH — it
# does not make the package resolvable by a separately invoked `node -e`.
CO2_TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$CO2_TMP_DIR"' EXIT

cat > "$CO2_TMP_DIR/report.mjs" <<'EOF'
import { readFileSync } from 'node:fs';
import { co2 } from '@tgwf/co2';

const reportPath = process.argv[2];
const greenHosting = process.argv[3] === 'true';
const report = JSON.parse(readFileSync(reportPath, 'utf8'));
const bytes = report.audits['total-byte-weight']?.numericValue;
if (typeof bytes !== 'number') {
  console.error('No total-byte-weight audit found in the Lighthouse report.');
  process.exit(1);
}

const emissions = new co2({ model: 'swd', rating: true });
const { total, rating } = emissions.perVisit(bytes, greenHosting);

console.log(`Transferred: ${(bytes / 1024).toFixed(1)} KB`);
console.log(`Estimated CO2 per page visit (${greenHosting ? 'green' : 'non-green'} hosting assumed): ${total.toFixed(3)} g (grade ${rating})`);
if (!greenHosting) {
  console.log('If hosting is confirmed green (https://www.thegreenwebfoundation.org/green-web-check/), re-run with GREEN_HOSTING=true for an accurate grade.');
}
EOF

CO2_INSTALL_LOG="$CO2_TMP_DIR/install.log"
if ! (cd "$CO2_TMP_DIR" && npm install --no-save --no-audit --no-fund "@tgwf/co2@$CO2_VERSION") >"$CO2_INSTALL_LOG" 2>&1; then
  echo "Failed to install @tgwf/co2@$CO2_VERSION:" >&2
  cat "$CO2_INSTALL_LOG" >&2
  exit 1
fi
node "$CO2_TMP_DIR/report.mjs" "$REPORT_JSON" "$GREEN_HOSTING"

echo "Full Lighthouse report: $REPORT_JSON"
