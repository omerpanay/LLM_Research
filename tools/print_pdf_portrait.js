// Print an HTML file to an A4 portrait PDF with page numbers and heading bookmarks.
// Usage: node tools/print_pdf_portrait.js <in.html> <out.pdf> [footer text]
// The footer defaults to the page <title>.
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const [inp, out] = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file://' + path.resolve(inp), { waitUntil: 'load' });
  const footer = (process.argv[4] || await page.title()).replace(/[<>&]/g, '');
  await page.emulateMedia({ media: 'print', colorScheme: 'light' });
  await page.pdf({ path: out, format: 'A4', printBackground: true, outline: true, tagged: true,
    preferCSSPageSize: true, displayHeaderFooter: true, headerTemplate: '<span></span>',
    footerTemplate: '<div style="font-size:8px;width:100%;text-align:center;color:#888">' + footer + ' · <span class="pageNumber"></span> / <span class="totalPages"></span></div>' });
  await browser.close();
})();
