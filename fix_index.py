# -*- coding: utf-8 -*-
"""Comprehensive fix for natrotu4/index.html"""
import re, sys

with open(r'F:\2fen\natrotu4\index.html', 'rb') as f:
    raw = f.read()

original_size = len(raw)
print(f'Original size: {original_size} bytes')

# Step 1: Remove BOM
if raw.startswith(b'\xef\xbb\xbf'):
    raw = raw[3:]
    print('[OK] Removed UTF-8 BOM')
else:
    print('[--] No BOM found')

# Step 2: Normalize line endings
raw = raw.replace(b'\r\n', b'\n').replace(b'\r', b'\n')
print('[OK] Normalized line endings to LF')

content = raw.decode('utf-8')

# Step 3: Find ALL script blocks
script_pattern = re.compile(r'<script>(.*?)</script>', re.DOTALL)
matches = list(script_pattern.finditer(content))
print(f'Found {len(matches)} script block(s):')
for i, m in enumerate(matches):
    inner = m.group(1).strip()
    print(f'  Block {i} ({m.start()}-{m.end()}, {len(inner)} chars): {repr(inner[:80])}')

# Step 4: Build consolidated script
# Keep the LAST (main game) script
main_script = matches[-1].group(1)

# Prepend short debug code from earlier scripts
if len(matches) > 1:
    for prev_m in matches[:-1]:
        prev = prev_m.group(1).strip()
        if len(prev) < 500:  # Short = debug, not game code
            if '</script>' in prev:
                prev = prev.replace('</script>', r'<\/script>')
            main_script = prev + '\n' + main_script
            print(f'[OK] Prepended debug code ({len(prev)} chars)')

# Step 5: Fix SVG data URLs
svg_fixed = re.sub(r'(data:image/svg\+xml,[^"\']*?)</svg>', r'\1<\/svg>', main_script)
if svg_fixed != main_script:
    main_script = svg_fixed
    print('[OK] Fixed unescaped </svg> in SVG URLs')

# Step 6: Escape literal </script> in JS
if '</script>' in main_script:
    main_script = main_script.replace('</script>', r'<\/script>')
    print('[OK] Escaped literal </script> in JS')

# Step 7: Fix API_BASE
old_api = "const API_BASE = 'https://natrotu4.up.railway.app'"
new_api = "const API_BASE = 'https://natrotu4-production.up.railway.app'"
if old_api in content:
    content = content.replace(old_api, new_api)
    print('[OK] Updated API_BASE to Railway production')
else:
    print('[--] API_BASE already correct or different')

# Step 8: Reconstruct - keep everything before first script + one consolidated script
# Remove ALL original script blocks and replace with one
first_start = matches[0].start()
last_end = matches[-1].end()
before = content[:first_start]
after = content[last_end:]
content = before + '<script>' + main_script + '</script>' + after
print(f'[OK] Consolidated {len(matches)} script blocks into 1')

# Step 9: Final BOM check
if content.startswith('\ufeff'):
    content = content[1:]
    print('[OK] Removed remaining BOM')

# Step 10: Verify
matches_after = list(script_pattern.finditer(content))
print(f'After fix: {len(matches_after)} script block(s), {len(content)} bytes')

# Write
with open(r'F:\2fen\natrotu4\index.html', 'w', encoding='utf-8', newline='\n') as f:
    f.write(content)

print(f'[DONE] Written: {len(content)} bytes (saved {original_size - len(content)} bytes)')
