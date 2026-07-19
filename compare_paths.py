# -*- coding: utf-8 -*-
import urllib.request

for path in ['/', '/index.html']:
    req = urllib.request.Request(
        'https://natrotu4-production.up.railway.app' + path,
        headers={'User-Agent': 'Mozilla/5.0', 'Cache-Control': 'no-cache'}
    )
    resp = urllib.request.urlopen(req, timeout=10)
    data = resp.read()
    print('Path: %s | Length: %d | Cache: %s | Content-Type: %s' % (
        path, len(data), resp.headers.get('Cache-Control', 'N/A'),
        resp.headers.get('Content-Type', 'N/A')))
    
    text = data.decode('utf-8', errors='replace')
    v551 = 'version: 551' in text
    print('  Has v551: %s | </script> count: %d' % (v551, text.count('</script>')))
    
    # Check response headers
    for h in ['Age', 'X-Cache', 'X-Cache-Hit', 'CF-Cache-Status', 'X-Railway-Request-Id']:
        v = resp.headers.get(h)
        if v:
            print('  %s: %s' % (h, v))
    print()
