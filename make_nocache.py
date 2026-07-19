# -*- coding: utf-8 -*-
# Add cache-busting meta tags and a big obvious comment to the HTML
# This will force the browser to re-fetch AND make it obvious if old version is cached
import urllib.request

resp = urllib.request.urlopen('https://natrotu4-production.up.railway.app/', timeout=10)
data = resp.read()
text = data.decode('utf-8', errors='replace')

# Add no-cache meta tags right after <head>
# And add a visible comment in the <body>
nocache_meta = '<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate"><meta http-equiv="Pragma" content="no-cache"><meta http-equiv="Expires" content="0">'

# Insert right after <head>
head_pos = text.find('<head>') + len('<head>')
text = text[:head_pos] + '\n' + nocache_meta + '\n' + text[head_pos:]

# Also add a visible banner at the top of body
banner = '\n<div id="cache-test-banner" style="background:#ff0;color:#000;padding:10px;text-align:center;font-size:20px;font-weight:bold;z-index:999999;position:relative;">CACHE TEST v551 - If you see this, you have the latest version!</div>\n'
body_pos = text.find('<body>') + len('<body>')
text = text[:body_pos] + banner + text[body_pos:]

# Write the updated content back
with open(r'F:\2fen\natrotu4\index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('Done. Content length: %d' % len(text))
print('Has no-cache meta: %s' % ('Cache-Control' in text))
print('Has cache test banner: %s' % ('cache-test-banner' in text))
