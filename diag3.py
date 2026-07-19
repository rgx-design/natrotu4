# -*- coding: utf-8 -*-
import urllib.request

url = 'https://natrotu4-production.up.railway.app/'
resp = urllib.request.urlopen(url, timeout=10)
text = resp.read().decode('utf-8', errors='replace')

# Extract script
s_start = text.find('<script>') + 8
e_end = text.rfind('</script>')
script = text[s_start:e_end]

# Check the FIRST 1500 chars (before showLogin at ~1405)
print('=== FIRST 1500 CHARS (before showLogin) ===')
print(repr(script[:1500]))
print()

# Check: is there an unclosed string or template literal?
# Look for backtick misuse
backtick_count = script[:1405].count('`')
print(f'Backticks before showLogin: {backtick_count}')
dollar_brace = script[:1405].count('${')
print(f'${"{"} template vars before showLogin: {dollar_brace}')

# Check for HTML comments inside JS
if '<!--' in script[:1405]:
    print('HTML comment found in JS!')
    idx = script.find('<!--')
    print(repr(script[idx:idx+50]))

# Check for --> without proper context
if '-->' in script[:1405]:
    print('--> found early in JS')
    idx = script.find('-->')
    print(repr(script[idx-30:idx+30]))

# Check structure: what's right before showLogin
print()
print('=== 50 chars BEFORE showLogin ===')
showlogin_pos = script.find('function showLogin')
print(repr(script[showlogin_pos-50:showlogin_pos]))

# Check: what char is at position 1400-1410
print()
print('=== Around position 1400-1410 ===')
print(repr(script[1390:1420]))
