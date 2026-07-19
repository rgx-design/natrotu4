# -*- coding: utf-8 -*-
import urllib.request

# Get Railway
resp = urllib.request.urlopen('https://natrotu4-production.up.railway.app/', timeout=10)
railway_data = resp.read()

# Get local
with open(r'F:\2fen\natrotu4\index.html', 'rb') as f:
    local_data = f.read()

print('Local: %d bytes, Railway: %d bytes' % (len(local_data), len(railway_data)))

# Compare byte by byte
min_len = min(len(local_data), len(railway_data))
diffs = []
for i in range(min_len):
    if local_data[i] != railway_data[i]:
        diffs.append(i)
        if len(diffs) <= 10:
            print('Diff at byte %d: local=%02x railway=%02x' % (i, local_data[i], railway_data[i]))
            print('  Local context:   %s' % str(local_data[max(0,i-20):i+20]))
            print('  Railway context:  %s' % str(railway_data[max(0,i-20):i+20]))

print('Total diffs: %d' % len(diffs))
