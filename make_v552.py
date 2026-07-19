# -*- coding: utf-8 -*-
import urllib.request, socket, hashlib

socket.setdefaulttimeout(8)

req = urllib.request.Request(
    'https://natrotu4-production.up.railway.app/',
    headers={'User-Agent': 'Mozilla/5.0', 'Cache-Control': 'no-cache'}
)
resp = urllib.request.urlopen(req, timeout=8)
data = resp.read()
text = data.decode('utf-8', errors='replace')
print('Original size: %d' % len(data))
print('First 100 chars: %s' % repr(text[:100]))

# Compute script hash
script_open = text.find('<script>') + 8
script_close = text.rfind('</script>')
script = text[script_open:script_close]
script_hash = hashlib.sha256(script.encode('utf-8')).hexdigest()[:12]
print('Script hash: %s' % script_hash)

# Count <body> occurrences
body_count = text.count('<body>')
print('<body> occurrences: %d' % body_count)
print('First <body> at: %d' % text.find('<body>'))

# The banner we want to add - SIMPLE, no placeholders
banner = (
    '<div id="v552" style="background:#cc0000;color:#fff;padding:12px;text-align:center;font-size:16px;font-weight:bold;position:fixed;top:0;left:0;right:0;z-index:9999999;">'
    'v552 | hash=' + script_hash + ' | Tell me what you see in this banner'
    '</div>'
)

# Just insert right after the <body> tag opening
body_tag_end = text.find('<body>') + len('<body>')
new_text = text[:body_tag_end] + banner + text[body_tag_end:]

# Also change version
new_text = new_text.replace('version: 551', 'version: 552')

print('New size: %d' % len(new_text))
print('Size difference: %+d' % (len(new_text) - len(data)))

with open(r'F:\2fen\natrotu4\index.html', 'w', encoding='utf-8') as f:
    f.write(new_text)
print('Saved OK')
print('Has v552 div:', 'id="v552"' in new_text)
