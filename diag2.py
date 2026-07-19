# -*- coding: utf-8 -*-
import urllib.request, re

url = 'https://natrotu4-production.up.railway.app/'
resp = urllib.request.urlopen(url, timeout=10)
text = resp.read().decode('utf-8', errors='replace')

# Extract the script
script_start = text.find('<script>') + 8
script_end = text.rfind('</script>')
script = text[script_start:script_end]
print(f'Script length: {len(script)}')

# Check for literal </script> inside script
if '</script>' in script:
    print('FOUND literal </script> in script!')
    idx = script.find('</script>')
    print(f'Context: {repr(script[max(0,idx-60):idx+20])}')
else:
    print('No literal </script> in script')

# Find showLogin definition
if 'function showLogin' in script:
    idx = script.find('function showLogin')
    print(f'showLogin defined at: {idx}')
    print(f'Context: {repr(script[idx:idx+100])}')
else:
    print('showLogin NOT found as function definition')
    # Maybe it's defined as const/let/var
    if 'showLogin' in script:
        matches = [(m.start(), m.end()) for m in re.finditer(r'showLogin', script)]
        print(f'showLogin appears {len(matches)} times, positions: {matches[:5]}')
        for pos in matches[:3]:
            print(f'  {repr(script[max(0,pos[0]-30):pos[1]+30])}')

# Find showRegister
if 'function showRegister' in script:
    print('showRegister found')
else:
    print('showRegister NOT found')

# Check for unclosed strings/brackets before showLogin
# Look for common JS syntax errors
lines = script.split('\n')
print(f'\nTotal lines: {len(lines)}')
# Print lines around showLogin
for i, line in enumerate(lines):
    if 'showLogin' in line and 'function' not in line and 'const' not in line and 'let' not in line and 'var' not in line:
        print(f'Line {i}: {repr(line[:100])}')
