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
