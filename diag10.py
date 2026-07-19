# -*- coding: utf-8 -*-
import urllib.request, re

resp = urllib.request.urlopen('https://natrotu4-production.up.railway.app/', timeout=10)
data = resp.read()
text = data.decode('utf-8', errors='replace')

s_start = text.find('<script>') + 8
e_end = text.rfind('</script>')
script = text[s_start:e_end]

# Find ALL code that runs at the TOP LEVEL of the script (not inside a function)
# Strategy: find all function definitions, then the code between them

func_positions = [(m.start(), m.group(1)) for m in re.finditer(r'function\s+(\w+)\s*\(', script)]
print('Functions found: %d' % len(func_positions))
for pos, name in func_positions:
    print('  %s at char %d' % (name, pos))

# Find the last function end
last_func_start = func_positions[-1][0]
last_func_name = func_positions[-1][1]

# Find where the last function ends
last_func_body_start = script.find('{', last_func_start)
depth = 0
for i in range(last_func_body_start, len(script)):
    if script[i] == '{': depth += 1
    elif script[i] == '}':
        depth -= 1
        if depth == 0:
            last_func_end = i + 1
            break

print()
print('Last function: %s (%d-%d)' % (last_func_name, last_func_start, last_func_end))

# Top-level code after all functions
top_level_after_funcs = script[last_func_end:]
print()
print('Top-level code after all functions (%d chars):' % len(top_level_after_funcs))
print(repr(top_level_after_funcs))

# Check: does the script end with proper closure?
print()
print('Script last 50 chars: %s' % repr(script[-50:]))

# Most important: check if </script> is properly at the end
raw_script_end = data[s_start+len('<script>'):]
raw_close = raw_script_end.find(b'</script>')
print()
print('Raw script content ends with: %s' % str(raw_script_end[raw_close-5:raw_close+20]))
