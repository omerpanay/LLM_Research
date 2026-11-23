// Render an HTML file to an A4-landscape PDF with Chromium. Usage: node tools/print_pdf.js <in.html> <out.pdf>
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const [inp, out] = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file://' + path.resolve(inp), { waitUntil: 'load' });
  await page.emulateMedia({ media: 'print', colorScheme: 'light' });
  await page.pdf({ path: out, format: 'A4', landscape: true, printBackground: true, outline: true, tagged: true,
    displayHeaderFooter: true, headerTemplate: '<span></span>',
    footerTemplate: '<div style="font-size:8px;width:100%;text-align:center;color:#888">Tez Araştırması TR-EN · <span class="pageNumber"></span> / <span class="totalPages"></span></div>',
    margin: { top: '10mm', bottom: '12mm', left: '10mm', right: '10mm' } });
  await browser.close();
})();
