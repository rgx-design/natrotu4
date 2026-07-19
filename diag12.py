# -*- coding: utf-8 -*-
import urllib.request

resp = urllib.request.urlopen('https://natrotu4-production.up.railway.app/', timeout=10)
data = resp.read()
text = data.decode('utf-8', errors='replace')

# Find ALL script tags
import re
opens = [(m.start(), m.group()) for m in re.finditer(r'<script', text)]
closes = [(m.start(), m.group()) for m in re.finditer(r'</script>', text)]
print('All <script tags:')
for pos, tag in opens:
    end = text.find('>', pos)
    print('  At %d: %s' % (pos, repr(text[pos:end+1])))

print()
print('All </script> tags:')
for pos, tag in closes:
    print('  At %d: %s' % (pos, repr(text[pos:pos+9])))

print()
print('Total <script: %d' % len(opens))
print('Total </script>: %d' % len(closes))

# Now let me check: what if the content type is being served as something that
# causes the browser to treat it as a module or with different parsing rules?
print()
print('=== HEADERS ===')
for k, v in resp.headers.items():
    if 'script' in k.lower() or 'type' in k.lower() or 'content' in k.lower():
        print('  %s: %s' % (k, v))
