# -*- coding: utf-8 -*-
import subprocess, urllib.request

# Get Railway HTML
resp = urllib.request.urlopen('https://natrotu4-production.up.railway.app/', timeout=10)
data = resp.read()
text = data.decode('utf-8', errors='replace')

s_start = text.find('<script>') + 8
e_end = text.rfind('</script>')
script = text[s_start:e_end]

# Write the script to a temp file
with open(r'F:\2fen\natrotu4\temp_script.js', 'w', encoding='utf-8') as f:
    f.write(script)

# Run it and check if showLogin is defined
node_code = '''
const fs = require('fs');
const script = fs.readFileSync('F:\\\\2fen\\\\natrotu4\\\\temp_script.js', 'utf8');
// Try to evaluate and check
try {
    // Create a function from the script
    const fn = new Function(script);
    // This won't execute, just parse
    console.log('Script parsed OK');
    // Check syntax more thoroughly
    // We need to extract function declarations
    const showLoginMatch = script.match(/function\\s+showLogin/);
    console.log('showLogin function found in source:', !!showLoginMatch);
    if (showLoginMatch) {
        console.log('At position:', showLoginMatch.index);
    }
} catch(e) {
    console.error('Error:', e.message);
}
'''
with open(r'F:\2fen\natrotu4\temp_check.js', 'w', encoding='utf-8') as f:
    f.write(node_code)

result = subprocess.run(['node', r'F:\2fen\natrotu4\temp_check.js'],
                       capture_output=True, text=True, timeout=10)
print('STDOUT:', result.stdout)
print('STDERR:', result.stderr[:500] if result.stderr else '')
print('Return code:', result.returncode)
