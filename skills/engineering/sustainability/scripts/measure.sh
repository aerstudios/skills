#!/usr/bin/env bash
# Portable CO2/weight measurement for any already-running build.
# Usage: measure.sh <url> [output-dir]
#
# Installs lighthouse and @tgwf/co2 on demand via npx — no project
# package.json changes required. Requires Node >=18 and network access
# to npm on first run.
set -euo pipefail

URL="${1:?Usage: measure.sh <url-to-a-running-build> [output-dir]}"
OUT_DIR="${2:-./sustainability-report}"
mkdir -p "$OUT_DIR"
REPORT_JSON="$OUT_DIR/lighthouse.json"

echo "Auditing $URL with Lighthouse..."
npx --yes lighthouse "$URL" \
  --output=json \
  --output-path="$REPORT_JSON" \
  --chrome-flags="--headless=new" \
  --only-categories=performance,seo \
  --quiet

npx --yes -p @tgwf/co2 node --input-type=module -e "
import { readFileSync } from 'node:fs';
import { co2 } from '@tgwf/co2';

const report = JSON.parse(readFileSync('$REPORT_JSON', 'utf8'));
const bytes = report.audits['total-byte-weight']?.numericValue;
if (!bytes) {
  console.error('No total-byte-weight audit found in the Lighthouse report.');
  process.exit(1);
}

const emissions = new co2({ model: 'swd', rating: true });
const { total, rating } = emissions.perVisit(bytes, false);

console.log(\`Transferred: \${(bytes / 1024).toFixed(1)} KB\`);
console.log(\`Estimated CO2 per page load (non-green hosting assumed): \${total.toFixed(3)} g (grade \${rating})\`);
console.log('If hosting is confirmed green (https://www.thegreenwebfoundation.org/green-web-check/), re-run perVisit(bytes, true) for an accurate grade.');
"

echo "Full Lighthouse report: $REPORT_JSON"
