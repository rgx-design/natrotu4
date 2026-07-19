# -*- coding: utf-8 -*-
import urllib.request

resp = urllib.request.urlopen('https://natrotu4-production.up.railway.app/', timeout=10)
data = resp.read()

# Find the actual first 50 bytes of the script content (after <script>)
script_open = data.find(b'<script>')
script_content_start = script_open + len(b'<script>')
script_content = data[script_content_start:]

# Find the </script> close
script_close = script_content.find(b'</script>')
raw_script = script_content[:script_close]

print('Total raw script bytes: %d' % len(raw_script))

# Check first 50 bytes
print('First 50 raw script bytes:')
print(str(raw_script[:50]))
print('Hex: %s' % raw_script[:50].hex())

# Now look at the LAST 100 bytes
print()
print('Last 100 raw script bytes:')
print(str(raw_script[-100:]))
print('Hex: %s' % raw_script[-100:].hex())

# Check: is there a NULL byte anywhere in the script?
null_count = raw_script.count(b'\x00')
print()
print('NULL bytes in script: %d' % null_count)

# Check for any invalid UTF-8 sequences
valid_utf8 = True
i = 0
invalid_positions = []
while i < len(raw_script):
    b = raw_script[i]
    if b > 127:
        # Multi-byte UTF-8
        if 0xC0 <= b <= 0xDF and i+1 < len(raw_script) and 0x80 <= raw_script[i+1] <= 0xBF:
            i += 2
        elif 0xE0 <= b <= 0xEF and i+2 < len(raw_script):
            i += 3
        elif 0xF0 <= b <= 0xF7 and i+3 < len(raw_script):
            i += 4
        else:
            if len(invalid_positions) < 5:
                invalid_positions.append(i)
            valid_utf8 = False
            i += 1
    else:
        i += 1

if invalid_positions:
    print('INVALID UTF-8 at positions: %s' % invalid_positions)
    for pos in invalid_positions[:3]:
        print('  Byte 0x%02x at %d, context: %s' % (raw_script[pos], pos, str(raw_script[max(0,pos-5):pos+10])))
else:
    print('All bytes are valid UTF-8')

# Most importantly: find what the RAW bytes are at position ~11898 (where error occurs)
# NOTE: 11898 is CHARACTER position, need to find corresponding BYTE position
text = data.decode('utf-8', errors='replace')
s_start = text.find('<script>') + 8
text_script = text[s_start:s_start + 11898]
raw_script_up_to_11898 = text_script.encode('utf-8')
actual_byte_pos = len(raw_script_up_to_11898)
print()
print('Character 11898 corresponds to byte %d in raw script' % actual_byte_pos)
print('Raw bytes around that position:')
chunk = raw_script[max(0, actual_byte_pos-20):actual_byte_pos+20]
print(str(chunk))
print('Hex: %s' % chunk.hex())
