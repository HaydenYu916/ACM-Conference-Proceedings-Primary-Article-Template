const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({viewport:{width:1504,height:464}});
  await p.goto('file://' + process.argv[2]); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(800);
  await p.pdf({path: process.argv[3], width:'1504px', height:'464px', printBackground:true, margin:{top:0,right:0,bottom:0,left:0}, pageRanges:'1'});
  await b.close();
})();
