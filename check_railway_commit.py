# -*- coding: utf-8 -*-
import urllib.request, socket, hashlib

socket.setdefaulttimeout(8)

# Check GitHub for the latest commit on main
try:
    req = urllib.request.Request(
        'https://api.github.com/repos/rgx-design/natrotu4/commits/main',
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    resp = urllib.request.urlopen(req, timeout=8)
    import json
    data = json.loads(resp.read())
    latest_sha = data['sha'][:7]
    print('GitHub main: %s' % latest_sha)
except Exception as e:
    print('GitHub check failed: %s' % e)
    latest_sha = None

# Check Railway's actual deployed content hash
try:
    req2 = urllib.request.Request(
        'https://natrotu4-production.up.railway.app/',
        headers={'User-Agent': 'Mozilla/5.0', 'Cache-Control': 'no-cache'}
    )
    resp2 = urllib.request.urlopen(req2, timeout=8)
    data2 = resp2.read()
    text2 = data2.decode('utf-8', errors='replace')
    
    # Compute hash of the full page
    page_hash = hashlib.sha256(data2).hexdigest()[:12]
    print('Railway page hash: %s' % page_hash)
    print('Railway page size: %d bytes' % len(data2))
    
    # Check version
    if 'version: 552' in text2:
        print('Railway: VERSION 552 - deployment SUCCEEDED')
    elif 'version: 551' in text2:
        print('Railway: VERSION 551 - OLD deployment')
    else:
        print('Railway: Unknown version')
        
except Exception as e:
    print('Railway check failed: %s' % e)
