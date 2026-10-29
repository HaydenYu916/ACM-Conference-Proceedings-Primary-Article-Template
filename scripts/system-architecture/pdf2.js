const { chromium } = require('playwright');
(async () => { const [inp,out,w,h]=process.argv.slice(2); const b=await chromium.launch(); const p=await b.newPage({viewport:{width:+w,height:+h}});
await p.goto('file://'+inp); await p.evaluate(()=>document.fonts.ready); await p.waitForTimeout(800);
await p.pdf({path:out,width:w+'px',height:h+'px',printBackground:true,margin:{top:0,right:0,bottom:0,left:0},pageRanges:'1'}); await b.close(); })();
