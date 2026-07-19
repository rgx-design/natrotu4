# -*- coding: utf-8 -*-
import urllib.request

url = 'https://natrotu4-production.up.railway.app/'
resp = urllib.request.urlopen(url, timeout=10)
data = resp.read()

s_start = data.find(b'<script>') + 8
e_end = data.rfind(b'</script>')
script_raw = data[s_start:e_end]

print('Script raw length:', len(script_raw))
print()

# Find the debug section at start
debug_section = script_raw[:200]
print('First 200 raw bytes:')
print(str(debug_section))
print()
print('Hex:')
for i in range(0, min(200, len(debug_section)), 50):
    print('  %3d: %s' % (i, debug_section[i:i+50].hex()))

# Look for actual newlines (0x0a) within the first 150 bytes
print()
print('Newline positions in first 150 bytes:', [i for i, b in enumerate(debug_section[:150]) if b == 0x0a])

# Check what's at position ~100 (after console.log line)
print()
print('Bytes 90-130:')
print(str(script_raw[90:130]))
print('Hex:', script_raw[90:130].hex())

# Find the \n in the window.addEventListener call
win_pos = script_raw.find(b'window.addEventListener')
if win_pos > 0:
    print()
    print('window.addEventListener at byte:', win_pos)
    print('Around it:')
    print(str(script_raw[max(0,win_pos-30):win_pos+80]))
    print('Hex:', script_raw[max(0,win_pos-30):win_pos+80].hex())
    # Check: is there a real newline after the first string?
    chunk = script_raw[win_pos-100:win_pos+20]
    for i, b in enumerate(chunk):
        if b == 0x0a:
            print('Real \\n found at offset %d from chunk start' % i)
    print()
    print('Chunk decoded:')
    try:
        print(repr(chunk.decode('utf-8')))
    except:
        print('Decode failed')
