# -*- coding: utf-8 -*-
import urllib.request

resp = urllib.request.urlopen('https://natrotu4-production.up.railway.app/', timeout=10)
data = resp.read()
text = data.decode('utf-8', errors='replace')

# Check the EXACT boundary between HTML and script
script_open_pos = data.find(b'<script>')
print('=== HTML right before <script> ===')
before = data[script_open_pos-200:script_open_pos]
print('Bytes: %s' % str(before))
print('Hex: %s' % before.hex())

# And the first few bytes of script content
print()
print('=== Script content FIRST 50 bytes ===')
script_content = data[script_open_pos + len(b'<script>'):]
print('Bytes: %s' % str(script_content[:50]))
print('Hex: %s' % script_content[:50].hex())

# Most important: check if there's a NO-BREAK SPACE or other invisible char
# before the script content
first_script_byte = script_content[0]
print()
print('First script byte: 0x%02x (%d)' % (first_script_byte, first_script_byte))
if first_script_byte > 127:
    print('WARNING: First byte is non-ASCII!')
    # Decode just the first char
    try:
        first_char = script_content[:1].decode('utf-8')
        print('First char: %r' % first_char)
    except:
        print('Cannot decode as UTF-8')

# Also: check the END of the script content
script_close_pos = script_content.find(b'</script>')
script_only = script_content[:script_close_pos]
print()
print('=== Script content LAST 50 bytes ===')
print('Bytes: %s' % str(script_only[-50:]))
print('Hex: %s' % script_only[-50:].hex())

# Check for invisible characters in script content
print()
print('=== Invisible char check in script ===')
invisible_count = 0
for i, b in enumerate(script_only):
    if b < 32 and b not in [10, 13, 9]:  # Allow \n \r \t
        if invisible_count < 5:
            print('  Invisible byte 0x%02x at position %d' % (b, i))
        invisible_count += 1
if invisible_count:
    print('Total invisible bytes: %d' % invisible_count)
else:
    print('No invisible bytes found')

# CHECK: Is the script content purely ASCII + valid UTF-8?
# If there are encoding errors, they would show as replacement chars
replacement_char_count = script_only.count('\ufffd')
print()
print('Replacement chars (UTF-8 errors): %d' % replacement_char_count)

# CRITICAL TEST: What if we write this script to a temp .js file and run it in Node?
import tempfile, os, subprocess
tmp = tempfile.NamedTemporaryFile(suffix='.js', delete=False, mode='wb')
tmp.write(script_only)
tmp.close()
print()
print('Written script to: %s' % tmp.name)
result = subprocess.run(['node', '--check', tmp.name], capture_output=True, text=True)
print('Node syntax check: returncode=%d' % result.returncode)
if result.stderr:
    print('Stderr: %s' % result.stderr[:500])
os.unlink(tmp.name)
