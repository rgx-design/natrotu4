# -*- coding: utf-8 -*-
import subprocess, tempfile, os, urllib.request

# Get Railway script
resp = urllib.request.urlopen('https://natrotu4-production.up.railway.app/', timeout=10)
data = resp.read()
text = data.decode('utf-8', errors='replace')
s_start = text.find('<script>') + 8
e_end = text.rfind('</script>')
script = text[s_start:e_end]

# Write to temp file and check with Node.js
with open(r'F:\2fen\natrotu4\temp_script.js', 'w', encoding='utf-8') as f:
    f.write(script)

# Use Node.js to check syntax
result = subprocess.run(['node', '--check', r'F:\2fen\natrotu4\temp_script.js'],
                       capture_output=True, text=True, timeout=10)
print('Return code:', result.returncode)
print('STDOUT:', result.stdout[:2000] if result.stdout else '(none)')
print('STDERR:', result.stderr[:2000] if result.stderr else '(none)')
