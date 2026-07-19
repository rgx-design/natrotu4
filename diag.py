# -*- coding: utf-8 -*-
import urllib.request, re

url = 'https://natrotu4-production.up.railway.app/'
resp = urllib.request.urlopen(url, timeout=10)
data = resp.read()
print(f'Size: {len(data)}, BOM: {data[:3].hex()}')
text = data.decode('utf-8', errors='replace')

# Count scripts
scripts = re.findall(r'<script>', text)
closes = re.findall(r'</script>', text)
print(f'Scripts: {len(scripts)}, Closes: {len(closes)}')

# Find first </script> position
first_close = text.find('</script>')
first_open = text.find('<script>')
print(f'First <script>: {first_open}, First </script>: {first_close}')

# Show raw bytes around first </script>
close_bytes = data[first_close-5:first_close+20]
print(f'Around first close: {close_bytes}')
print(f'Hex: {close_bytes.hex()}')

# Check for BOM
if data[:3] == b'\xef\xbb\xbf':
    print('HAS BOM!')
else:
    print('No BOM - OK')

# Check version
if 'version: 548' in text:
    print('NEW VERSION (548) - deployed!')
elif 'version: 548771f' in text:
    print('OLD VERSION (548771f) - not yet deployed')
else:
    print('Unknown version')

# Show script content
if first_open >= 0 and first_close >= 0:
    script_content = text[first_open+8:first_close]
    print(f'First script content (first 200 chars): {repr(script_content[:200])}')
