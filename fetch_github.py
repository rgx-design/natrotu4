# -*- coding: utf-8 -*-
# Fetch RAW index.html from GitHub, apply v552 changes, save locally
import urllib.request, socket, hashlib

socket.setdefaulttimeout(10)

# Fetch raw GitHub file
url = 'https://raw.githubusercontent.com/rgx-design/natrotu4/main/index.html'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    resp = urllib.request.urlopen(req, timeout=10)
    data = resp.read()
    print('GitHub raw fetch: %d bytes' % len(data))
except Exception as e:
    print('GitHub fetch failed: %s' % e)
    import sys; sys.exit(1)

text = data.decode('utf-8', errors='replace')

# Compute script hash
so = text.find('<script>') + 8
sc = text.rfind('</script>')
script = text[so:sc]
h = hashlib.sha256(script.encode('utf-8')).hexdigest()[:12]
print('Script hash: %s' % h)

# Add banner right after <body>
body_end = text.find('<body>') + 6
banner = '<div id="v552banner" style="background:#cc0000;color:#fff;padding:12px;text-align:center;font-size:16px;font-weight:bold;position:fixed;top:0;left:0;right:0;z-index:9999999;">v552 | hash=' + h + ' | Tell me what you see</div>'
new_text = text[:body_end] + banner + text[body_end:]

# Update version string
if 'version: 551' in new_text:
    new_text = new_text.replace('version: 551', 'version: 552')
elif 'version: 552' in new_text:
    print('Already v552!')
else:
    print('WARNING: no version string found')

print('Original: %d, New: %d, Diff: %+d' % (len(data), len(new_text), len(new_text)-len(data)))

with open(r'F:\2fen\natrotu4\index.html', 'w', encoding='utf-8') as f:
    f.write(new_text)
print('Written. v552=%s' % ('version: 552' in new_text))
