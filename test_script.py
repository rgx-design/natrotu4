# -*- coding: utf-8 -*-
import urllib.request, tempfile, os, subprocess

resp = urllib.request.urlopen('https://natrotu4-production.up.railway.app/', timeout=10)
data = resp.read()
text = data.decode('utf-8', errors='replace')

script_open = text.find('<script>') + 8
script_close = text.rfind('</script>')
script = text[script_open:script_close]

print('Script length: %d' % len(script))
print('Script SHA256: %s' % __import__('hashlib').sha256(script.encode('utf-8')).hexdigest())

# Write to temp .js file
tmp = tempfile.NamedTemporaryFile(suffix='.js', delete=False, mode='w', encoding='utf-8')
tmp.write(script)
tmp.close()
print('Written to: %s' % tmp.name)

# Run the script with Node.js - capture ALL output
result = subprocess.run(
    ['node', '-e', '''
const fs = require('fs');
const script = fs.readFileSync('%s', 'utf8');
// Try to evaluate the script
try {
    eval(script);
    console.log('=== EVALUATED OK ===');
    console.log('typeof showLogin:', typeof showLogin);
    console.log('typeof doLogin:', typeof doLogin);
    console.log('typeof updateHeaderAuth:', typeof updateHeaderAuth);
} catch(e) {
    console.error('EVAL ERROR:', e.message);
    console.error('At line:', e.lineNumber);
    console.error('At column:', e.columnNumber);
}
''' % tmp.name.replace('\\', '\\\\')],
    capture_output=True, text=True, timeout=10
)
print()
print('STDOUT:', result.stdout[:2000])
print('STDERR:', result.stderr[:500] if result.stderr else '')
print('Return code:', result.returncode)

os.unlink(tmp.name)
