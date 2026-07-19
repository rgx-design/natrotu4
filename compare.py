# -*- coding: utf-8 -*-
# Compare local vs Railway file structures
content_local = open(r'F:\2fen\natrotu4\index.html', 'r', encoding='utf-8').read()
script_start_local = content_local.find('<script>') + 8
script_end_local = content_local.rfind('</script>')
local_script = content_local[script_start_local:script_end_local]

import urllib.request
resp = urllib.request.urlopen('https://natrotu4-production.up.railway.app/', timeout=10)
data = resp.read()
text_railway = data.decode('utf-8', errors='replace')
script_start_r = text_railway.find('<script>') + 8
script_end_r = text_railway.rfind('</script>')
railway_script = text_railway[script_start_r:script_end_r]

print('LOCAL: script starts at char %d, length %d' % (script_start_local, len(local_script)))
print('RAILWAY: script starts at char %d, length %d' % (script_start_r, len(railway_script)))
print()
print('LOCAL first 100 chars of script:')
print(repr(local_script[:100]))
print()
print('RAILWAY first 100 chars of script:')
print(repr(railway_script[:100]))
print()

# The scripts should be identical since they have the same byte length
# But the showLogin position is very different!
# Let's check: maybe the local file has a DIFFERENT structure
print('LOCAL <script> at char: %d' % (script_start_local - 8))
print('RAILWAY <script> at char: %d' % (script_start_r - 8))
print()
# Check the HTML before the script
local_before = content_local[:script_start_local-8]
railway_before = text_railway[:script_start_r-8]
print('LOCAL HTML before script: %d chars' % len(local_before))
print('RAILWAY HTML before script: %d chars' % len(railway_before))
print()
# Check if they match
if local_before == railway_before:
    print('HTML BEFORE SCRIPT: IDENTICAL')
else:
    print('HTML BEFORE SCRIPT: DIFFERENT!')
    print('LOCAL first 100: %s' % repr(local_before[:100]))
    print('RAILWAY first 100: %s' % repr(railway_before[:100]))
    print()
    # Find first difference
    for i in range(min(len(local_before), len(railway_before))):
        if local_before[i] != railway_before[i]:
            print('First diff at char %d: local=%r railway=%r' % (i, local_before[i], railway_before[i]))
            print('Context: local=%s' % repr(local_before[max(0,i-30):i+30]))
            print('Context: railway=%s' % repr(railway_before[max(0,i-30):i+30]))
            break

# Most important: what is at char 17470 in local file (showLogin)?
print()
print('=== Around showLogin in LOCAL file ===')
print(repr(content_local[17450:17550]))
print()
# What is at char 1405 in Railway file (showLogin)?
print('=== Around showLogin in RAILWAY file ===')
print(repr(text_railway[1395:1495]))
