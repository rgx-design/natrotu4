# -*- coding: utf-8 -*-
import urllib.request

req = urllib.request.Request(
    'https://natrotu4-production.up.railway.app/',
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Cache-Control': 'no-cache'
    }
)
resp = urllib.request.urlopen(req, timeout=10)
data = resp.read()

print('=== Cache Headers ===')
print('Cache-Control:', resp.headers.get('Cache-Control'))
print('Pragma:', resp.headers.get('Pragma'))
print('Expires:', resp.headers.get('Expires'))
print('Content-Length:', resp.headers.get('Content-Length'))
print()

# Check version
text = data.decode('utf-8', errors='replace')
if 'version: 551' in text:
    print('SCRIPT VERSION: 551')
elif 'version: 548' in text:
    print('SCRIPT VERSION: 548 (OLD - still cached!)')
else:
    print('SCRIPT VERSION: UNKNOWN')

# Check for </script> bug in full HTML
import re
closes = [m.start() for m in re.finditer(r'</script>', text)]
print('Total </script> in HTML: %d' % len(closes))
for pos in closes:
    context = text[max(0,pos-30):pos+9]
    print('  At %d: %s' % (pos, repr(context)))

# Check for the no-cache banner
if 'cache-test-banner' in text:
    print('CACHE BANNER: present')
else:
    print('CACHE BANNER: missing (old version)')
