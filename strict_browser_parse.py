# -*- coding: utf-8 -*-
# STRICT browser simulation - find ALL script blocks including malformed ones
import urllib.request, re

resp = urllib.request.urlopen('https://natrotu4-production.up.railway.app/', timeout=10)
data = resp.read()
text = data.decode('utf-8', errors='replace')

print('=== METHOD 1: regex (re.DOTALL) ===')
matches = list(re.finditer(r'<script[^>]*>(.*?)</script>', text, re.DOTALL | re.IGNORECASE))
print('Found: %d' % len(matches))
for i, m in enumerate(matches):
    content = m.group(1)
    bug = '</script>' in content
    print('  #%d: len=%d bug=%s' % (i+1, len(content), bug))

print()
print('=== METHOD 2: Case-insensitive scan like real browser ===')
# Browser: find '<script' then find '>' then find '</script>'
lower = text.lower()
pos = 0
scripts_found = []
while True:
    idx = lower.find('<script', pos)
    if idx == -1:
        break
    # Find closing '>'
    close_gt = text.find('>', idx)
    if close_gt == -1:
        break
    # Now search for '</script>' after this '>'
    end_idx = lower.find('</script>', close_gt)
    if end_idx == -1:
        break
    content = text[close_gt+1:end_idx]
    scripts_found.append({
        'open_at': idx,
        'close_tag_at': end_idx,
        'content_len': len(content),
        'has_bug': '</script>' in content,
        'first_50': content[:50],
        'has_showLogin': 'function showLogin' in content
    })
    pos = end_idx + 9

print('Found: %d' % len(scripts_found))
for s in scripts_found:
    print('  open=%d close=%d len=%d bug=%s has_showLogin=%s' % (
        s['open_at'], s['close_tag_at'], s['content_len'], s['has_bug'], s['has_showLogin']))
    print('  first_50: %s' % repr(s['first_50']))

# Most importantly: check for ANY embedded </script> in content
print()
print('=== EMBEDDED </script> CHECK ===')
for i, s in enumerate(scripts_found):
    embeds = [m.start() for m in re.finditer(r'</script>', s['first_50'] + ' ' + s['content'][50:10000])]
    if s['content'].count('</script>') > 0:
        print('  Script #%d: FOUND embedded </script>!' % (i+1))
        for pos in [j for j in range(len(s['content'])) if s['content'][j:j+9] == '</script>']:
            print('    At offset %d: %s' % (pos, repr(s['content'][max(0,pos-30):pos+20])))
    else:
        print('  Script #%d: clean' % (i+1))

# Also check the exact bytes around the <script> tag opening
print()
print('=== BYTES AROUND <script> OPENING ===')
script_pos = data.find(b'<script>')
print('Total occurrences of <script>: %d' % data.lower().count(b'<script>'))
print('First <script> at byte: %d' % script_pos)
print('Bytes around first <script>:')
print('  Before: %s' % str(data[max(0,script_pos-5):script_pos]).hex())
print('  Tag: %s' % str(data[script_pos:script_pos+8]).hex())
print('  After: %s' % str(data[script_pos+8:script_pos+20]).hex())
