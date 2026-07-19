# -*- coding: utf-8 -*-
# Read the local index.html and create a patched version with extra diagnostics
content = open(r'F:\2fen\natrotu4\index.html', 'r', encoding='utf-8').read()
script_start = content.find('<script>') + 8
script_end = content.rfind('</script>')
script = content[script_start:script_end]

# Show first 300 chars and last 200 chars of script
print('=== SCRIPT FIRST 300 ===')
print(repr(script[:300]))
print()
print('=== SCRIPT LAST 200 ===')
print(repr(script[-200:]))

# Also show what the function declarations look like in the script
print()
print('=== showLogin definition context ===')
sl_pos = script.find('function showLogin')
print(repr(script[sl_pos-50:sl_pos+150]))
