# -*- coding: utf-8 -*-
import urllib.request

resp = urllib.request.urlopen('https://natrotu4-production.up.railway.app/', timeout=10)
data = resp.read()

text = data.decode('utf-8', errors='replace')
s_start = text.find('<script>') + 8
e_end = text.rfind('</script>')
script = text[s_start:e_end]

# What's at char 11898?
pos = 11898
print('=== Around char 11898 (REPORTED error position) ===')
print(repr(script[pos-80:pos+80]))
print()

# What's 500 chars before and after
print('=== 500 chars BEFORE 11898 ===')
chunk_before = script[max(0,pos-500):pos]
print(repr(chunk_before))
print()
print('=== 500 chars AFTER 11898 ===')
chunk_after = script[pos:pos+500]
print(repr(chunk_after))

# Now let's try a different approach: find ALL function definitions
import re
funcs = re.findall(r'function\s+(\w+)', script)
print()
print('All function names defined in script (%d total):' % len(funcs))
for f in funcs:
    idx = script.find('function ' + f)
    print('  %s at char %d' % (f, idx))
