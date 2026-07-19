# -*- coding: utf-8 -*-
import urllib.request

url = 'https://natrotu4-production.up.railway.app/'
resp = urllib.request.urlopen(url, timeout=10)
data = resp.read()

s_start = data.find(b'<script>') + 8
e_end = data.rfind(b'</script>')
script_raw = data[s_start:e_end]

print('Script raw length:', len(script_raw))

# The scan.py found unclosed string at byte 492
# Let's examine the area around byte 492
print()
print('=== Around byte 492 ===')
print('Raw bytes 450-530:')
chunk = script_raw[450:530]
print(str(chunk))
print('Hex:', chunk.hex())

# Decode this area
try:
    decoded = chunk.decode('utf-8')
    print('Decoded: %s' % repr(decoded))
except Exception as e:
    print('Decode error:', e)
    # Try latin-1
    print('Latin-1: %s' % repr(chunk.decode('latin-1')))

# Let's also look at the WHOLE first 600 bytes to understand the structure
print()
print('=== First 600 bytes decoded ===')
try:
    first600 = script_raw[:600].decode('utf-8')
    print(repr(first600))
except Exception as e:
    print('Error:', e)

# Now look for the FIRST syntax error in the whole script
# Strategy: find the closing of the first string after char 50
# The debug log string ends at the first );
print()
print('=== Finding first ; in raw script ===')
# Find position of first semicolon after byte 50
semi_pos = script_raw.find(b';')
print('First semicolon at byte: %d' % semi_pos)
print('Context: %s' % str(script_raw[max(0,semi_pos-20):semi_pos+30]))

# Check: after the first ; is there a valid statement?
# Look for the pattern: '";' followed by valid JS
after_first_semi = script_raw[semi_pos+1:semi_pos+20]
print('After first ; : %s' % str(after_first_semi))
print('After first ; hex: %s' % after_first_semi.hex())
