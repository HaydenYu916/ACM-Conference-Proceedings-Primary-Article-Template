import re,os,sys
F,inp,out=sys.argv[1:4]
s=open(inp).read()
faces=""
for sub in ["latin","latin-ext","greek"]:
  for w in [400,500,600,700]:
    for st in ["normal","italic"]:
      fn=f"{F}/source-sans-3-{sub}-{w}-{st}.woff2"
      if os.path.exists(fn):
        faces+=f"@font-face{{font-family:'SS3P';font-weight:{w};font-style:{st};src:url('file://{fn}') format('woff2');}}\n"
s=re.sub(r'<link href="https://fonts.googleapis.com[^>]*>', '<style>'+faces+'</style>', s)
s=re.sub(r"font-family:\s*'Source Sans 3'","font-family:'SS3P'",s)
open(out,'w').write(s)
