# -*- coding: utf-8 -*-
import urllib.request

resp = urllib.request.urlopen('https://natrotu4-production.up.railway.app/', timeout=10)
data = resp.read()

script_open = data.find(b'<script>') + len(b'<script>')
script_close = data.find(b'</script>')
raw_script = data[script_open:script_close]

# Find "function showLogin" position in raw bytes
target = b'function showLogin'
pos = raw_script.find(target)
print('function showLogin at raw byte: %d' % pos)

# Show 100 bytes BEFORE the function declaration
print()
print('=== 100 bytes BEFORE showLogin ===')
chunk = raw_script[max(0, pos-100):pos]
print('Hex: %s' % chunk.hex())
print('Text: %s' % str(chunk))

# Show 100 bytes AFTER 
print()
print('=== 100 bytes AFTER showLogin ===')
chunk2 = raw_script[pos:pos+100]
print('Hex: %s' % chunk2.hex())
print('Text: %s' % str(chunk2))

# Most importantly: check if the bytes immediately before "function showLogin"
# contain any unexpected characters (like stray quotes, backslashes, etc.)
print()
print('=== Exact bytes at boundary ===')
before_func = raw_script[pos-5:pos]
print('5 bytes before: %s | Hex: %s' % (str(before_func), before_func.hex()))

# Run Node syntax check on raw bytes
import tempfile, os, subprocess
tmp = tempfile.NamedTemporaryFile(suffix='.js', delete=False, mode='wb')
tmp.write(raw_script)
tmp.close()

result = subprocess.run(['node', '--check', tmp.name], capture_output=True, text=True, timeout=10)
print()
print('Node syntax check returncode: %d' % result.returncode)
if result.stderr:
    print('Stderr: %s' % result.stderr[:300])
if result.returncode != 0:
    # Find the actual error
    result2 = subprocess.run(['node', '--check', tmp.name], capture_output=True, text=True, timeout=10)
    print('Full stderr: %s' % result2.stderr[:500])
os.unlink(tmp.name)
