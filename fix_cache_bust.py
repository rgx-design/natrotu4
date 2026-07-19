# -*- coding: utf-8 -*-
import urllib.request, time

# Download the current Railway index.html
resp = urllib.request.urlopen('https://natrotu4-production.up.railway.app/', timeout=10)
data = resp.read()
text = data.decode('utf-8', errors='replace')

print('Current length: %d' % len(text))

# Add cache-busting version to ALL resource references
# This ensures CDN sees a different URL and fetches fresh content
version = '552'
bust = '?v=%s&t=%d' % (version, int(time.time()))

# Add version to <link> tags (CSS)
import re
text = re.sub(r'(<link[^>]+href=["\'])([^\"\']+)(["\'])',
    lambda m: m.group(1) + m.group(2) + bust + m.group(3),
    text)

# Add version to <script src=> tags
text = re.sub(r'(<script[^>]+src=["\'])([^\"\']+)(["\'])',
    lambda m: m.group(1) + m.group(2) + bust + m.group(3),
    text)

# Add a visible version banner so user can confirm they're on latest
banner = '\n<!-- VERSION %s - if you see this, you're on the latest! -->\n' % version
head_pos = text.find('<head>') + len('<head>')
text = text[:head_pos] + banner + text[head_pos:]

# Save locally for pushing
with open(r'F:\2fen\natrotu4\index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('Saved with version %s. New length: %d' % (version, len(text)))
print('Has version comment: %s' % ('VERSION %s' % version in text))

# Verify
resp2 = urllib.request.urlopen('https://natrotu4-production.up.railway.app/', timeout=10)
data2 = resp2.read()
text2 = data2.decode('utf-8', errors='replace')
print('Railway still at length: %d' % len(text2))
print('Railway has VERSION comment: %s' % ('VERSION 552' in text2))
