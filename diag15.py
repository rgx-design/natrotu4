# -*- coding: utf-8 -*-
import urllib.request

req = urllib.request.Request(
    'https://natrotu4-production.up.railway.app/',
    headers={
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
)
resp = urllib.request.urlopen(req, timeout=10)

print('=== ALL RESPONSE HEADERS ===')
for k, v in resp.headers.items():
    print('  %s: %s' % (k, v))

data = resp.read()
print()
print('Content length: %d' % len(data))
text = data.decode('utf-8', errors='replace')

# Check for no-cache headers
print()
print('Cache-Control: %s' % resp.headers.get('Cache-Control'))
print('Pragma: %s' % resp.headers.get('Pragma'))
print('Expires: %s' % resp.headers.get('Expires'))
print('ETag: %s' % resp.headers.get('ETag'))
print('Last-Modified: %s' % resp.headers.get('Last-Modified'))

# Most importantly: check the script content
script_open = text.find('<script>') + 8
script_close = text.rfind('</script>')
script = text[script_open:script_close]
print()
print('Script version check:')
if '[DEBUG] Script tag found, version: 551' in script:
    print('✅ v551 detected in script')
elif '[DEBUG] Script tag found, version: 548' in script:
    print('❌ v548 (OLD) detected in script')
else:
    print('Unknown version')

# Check for </script> inside script
if '</script>' in script:
    print('❌ FOUND </script> inside script content!')
else:
    print('✅ No </script> inside script content')
