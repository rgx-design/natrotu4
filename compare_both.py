# -*- coding: utf-8 -*-
import urllib.request, socket, hashlib

socket.setdefaulttimeout(10)

# Fetch from GitHub raw
req1 = urllib.request.Request(
    'https://raw.githubusercontent.com/rgx-design/natrotu4/main/index.html',
    headers={'User-Agent': 'Mozilla/5.0'}
)
gh_resp = urllib.request.urlopen(req1, timeout=10)
gh_data = gh_resp.read()
print('GitHub: %d bytes, hash=%s' % (len(gh_data), hashlib.md5(gh_data).hexdigest()))

# Fetch from Railway
req2 = urllib.request.Request(
    'https://natrotu4-production.up.railway.app/',
    headers={'User-Agent': 'Mozilla/5.0', 'Cache-Control': 'no-cache'}
)
rail_resp = urllib.request.urlopen(req2, timeout=10)
rail_data = rail_resp.read()
print('Railway: %d bytes, hash=%s' % (len(rail_data), hashlib.md5(rail_data).hexdigest()))

# Compare byte by byte
if gh_data == rail_data:
    print('IDENTICAL - both %d bytes' % len(gh_data))
else:
    print('DIFFERENT!')
    # Find first difference
    min_len = min(len(gh_data), len(rail_data))
    for i in range(min_len):
        if gh_data[i] != rail_data[i]:
            print('First diff at byte %d: GH=0x%02x RR=0x%02x' % (i, gh_data[i], rail_data[i]))
            print('GH context: %s' % str(gh_data[max(0,i-20):i+20]))
            print('RR context: %s' % str(rail_data[max(0,i-20):i+20]))
            break
    if len(gh_data) != len(rail_data):
        print('Length diff: GH=%d RR=%d' % (len(gh_data), len(rail_data)))
