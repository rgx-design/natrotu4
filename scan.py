# -*- coding: utf-8 -*-
import urllib.request, re

url = 'https://natrotu4-production.up.railway.app/'
resp = urllib.request.urlopen(url, timeout=10)
data = resp.read()

# Work with raw bytes to avoid UTF-8 decode issues
text = data.decode('utf-8', errors='replace')
raw = data

s_start = text.find('<script>') + 8
e_end = text.rfind('</script>')
script_text = text[s_start:e_end]

# Find showLogin
sl_pos = script_text.find('function showLogin')
print('showLogin at char: %d' % sl_pos)

# Find exact byte position of showLogin in raw bytes
script_raw = raw[s_start:e_end]
func_bytes = b'function showLogin'
byte_pos = script_raw.find(func_bytes)
print('showLogin at byte: %d' % byte_pos)

# Get 200 bytes BEFORE showLogin (from raw)
before_slice = script_raw[max(0, byte_pos-200):byte_pos]
print()
print('=== 200 raw bytes BEFORE showLogin ===')
print('Hex: %s' % before_slice.hex())
# Decode just that portion
try:
    decoded = before_slice.decode('utf-8')
    print('Decoded: %s' % repr(decoded))
except:
    print('Decode failed, try latin-1: %s' % repr(before_slice.decode('latin-1')))

# Check for: HTML comment <!-- inside script
if b'<!--' in script_raw[:byte_pos]:
    idx = script_raw[:byte_pos].rfind(b'<!--')
    print()
    print('HTML comment found at byte %d!' % idx)
    print('Context: %s' % str(script_raw[idx:idx+50]))

# Check for --> before showLogin
if b'-->' in script_raw[:byte_pos]:
    idx = script_raw[:byte_pos].rfind(b'-->')
    print()
    print('--> found at byte %d!' % idx)
    print('Context: %s' % str(script_raw[idx:idx+30]))

# Check for any unescaped </script anywhere in script
if b'</script' in script_raw:
    print()
    print('!! </script found in script at:', script_raw.find(b'</script'))
    idx = script_raw.find(b'</script')
    print('Context: %s' % str(script_raw[idx-20:idx+30]))

# Check: what are the last 50 chars BEFORE showLogin in raw?
print()
print('=== Last 50 raw bytes before showLogin ===')
print(str(script_raw[byte_pos-50:byte_pos]))
print('Hex: %s' % script_raw[byte_pos-50:byte_pos].hex())

# Try to parse the script with simple brace counting to find mismatch
# Look for unclosed strings, template literals, regex
print()
print('=== Checking for unclosed strings before showLogin ===')
chunk = script_raw[:byte_pos]
# Check for unclosed template literals (backtick without matching)
backtick_count = chunk.count(b'`')
# Count template expressions ${}
template_expr_count = chunk.count(b'${')
print('Backticks: %d, Template expressions: %d' % (backtick_count, template_expr_count))

# Check for unclosed single/double quotes
# Find positions of quotes
in_string = False
string_char = None
string_start = 0
errors_found = []
i = 0
while i < len(chunk):
    c = chunk[i:i+1]
    if not in_string:
        if c in (b"'", b'"', b'`'):
            in_string = True
            string_char = c
            string_start = i
        elif c == b'/' and i+1 < len(chunk) and chunk[i+1:i+2] == b'/':
            # Line comment - skip to end of line
            while i < len(chunk) and chunk[i] != ord('\n'):
                i += 1
    else:
        if c == string_char and chunk[i-1:i] != b'\\':
            in_string = False
        elif c == b'\n' and string_char != b'`':
            # Unclosed string
            errors_found.append(('unclosed string', string_start, i, chunk[string_start:string_start+30]))
            in_string = False
    i += 1

if errors_found:
    for err in errors_found:
        print('Error: %s at %d: %s' % (err[0], err[1], str(err[3])))
else:
    print('No unclosed strings found')

if in_string:
    print('Still in string at end of chunk!')
    print('String started at: %d, content: %s' % (string_start, str(chunk[string_start:string_start+50])))
