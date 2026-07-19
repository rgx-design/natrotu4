# -*- coding: utf-8 -*-
import urllib.request, re

resp = urllib.request.urlopen('https://natrotu4-production.up.railway.app/', timeout=10)
data = resp.read()
text = data.decode('utf-8', errors='replace')

# Check for ANY external script sources
print('=== External script sources ===')
for m in re.finditer(r'<script[^>]+src=[^>]+>', text):
    print('  %s' % m.group())

# Check for any other external resources that might have cached old versions
print()
print('=== External resources with potential cache ===')
for m in re.finditer(r'(src|href)=["\']([^"\']+)["\']', text):
    url = m.group(2)
    if not url.startswith('data:') and not url.startswith('http') and not url.startswith('//'):
        print('  %s: %s' % (m.group(1), url))

# Most important: check ALL script tag contents for </script>
print()
print('=== All script blocks ===')
for i, m in enumerate(re.finditer(r'<script[^>]*>(.*?)</script>', text, re.DOTALL)):
    content = m.group(1)
    has_bug = '</script>' in content
    print('Script #%d: %d chars, has_bug=%s' % (i+1, len(content), has_bug))
    if has_bug:
        # Find where the bug is
        for pos in [j for j in range(len(content)) if content[j:j+9] == '</script>']:
            print('  BUG at offset %d: %s' % (pos, repr(content[max(0,pos-30):pos+20])))

# Check img onerror attributes for </svg>
print()
print('=== img onerror attributes ===')
for m in re.finditer(r'<img[^>]+onerror=[^>]+>', text):
    attr = m.group()
    if '</svg>' in attr or '</script>' in attr:
        print('  POTENTIAL BUG: %s' % repr(attr[:200]))
    else:
        print('  OK: %s' % repr(attr[:100]))
