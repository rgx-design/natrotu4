# -*- coding: utf-8 -*-
import urllib.request

resp = urllib.request.urlopen('https://natrotu4-production.up.railway.app/', timeout=10)
print('=== RESPONSE HEADERS ===')
for k, v in resp.headers.items():
    print('  %s: %s' % (k, v))

data = resp.read()
print()
print('=== PAGE SIZE: %d bytes ===' % len(data))

text = data.decode('utf-8', errors='replace')

# Find button definitions with showLogin in HTML
import re
# Find ALL function references in the HTML (before script)
before_script = text[:text.find('<script>')]
print()
print('=== showLogin reference in HTML ===')
matches = list(re.finditer(r'show\w+', before_script))
for m in matches:
    start = max(0, m.start()-30)
    end = min(len(before_script), m.end()+30)
    print('  At %d: ...%s...' % (m.start(), repr(before_script[start:end])))

# Now check: what happens if I write this script to a file and open it in a browser?
# First, let me verify the script content matches what we expect
s_start = text.find('<script>') + 8
e_end = text.rfind('</script>')
script = text[s_start:e_end]

print()
print('=== SCRIPT VERIFICATION ===')
print('Script length: %d chars' % len(script))
print('Has showLogin: %s' % ('function showLogin' in script))
print('Has doLogin: %s' % ('function doLogin' in script))
print('Script starts: %s' % repr(script[:100]))
print('Script ends: %s' % repr(script[-100:]))

# Count all function definitions
funcs = re.findall(r'function\s+\w+\s*\(', script)
print('Function count: %d' % len(funcs))
print('Functions: %s' % [f[9:-2] for f in funcs])
