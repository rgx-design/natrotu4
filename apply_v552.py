# -*- coding: utf-8 -*-
# Verify the local file is correct, then apply v552 changes
import hashlib

with open(r'F:\2fen\natrotu4\index.html', 'rb') as f:
    data = f.read()

print('Local file: %d bytes, hash=%s' % (len(data), hashlib.md5(data).hexdigest()))

text = data.decode('utf-8', errors='replace')

# Compute script hash
so = text.find('<script>') + 8
sc = text.rfind('</script>')
script = text[so:sc]
h = hashlib.sha256(script.encode('utf-8')).hexdigest()[:12]
print('Script hash: %s' % h)
print('Script length: %d' % len(script))

# Add banner right after <body>
body_end = text.find('<body>') + 6
banner = '<div id="v552banner" style="background:#cc0000;color:#fff;padding:12px;text-align:center;font-size:16px;font-weight:bold;position:fixed;top:0;left:0;right:0;z-index:9999999;">v552 | hash=' + h + ' | Tell me what you see in the BANNER at top of screen</div>'
new_text = text[:body_end] + banner + text[body_end:]

# Update version string
new_text = new_text.replace('version: 551', 'version: 552')

print()
print('Original: %d' % len(data))
print('Modified: %d' % len(new_text))
print('Change: %+d' % (len(new_text) - len(data)))
print()
print('Has v552banner:', 'v552banner' in new_text)
print('Version is 552:', 'version: 552' in new_text)
print('Has old 551:', 'version: 551' in new_text)

with open(r'F:\2fen\natrotu4\index.html', 'w', encoding='utf-8') as f:
    f.write(new_text)
print()
print('Written successfully')
