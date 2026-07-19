# -*- coding: utf-8 -*-
import urllib.request

url = 'https://natrotu4-production.up.railway.app/'
resp = urllib.request.urlopen(url, timeout=10)
data = resp.read()
text = data.decode('utf-8', errors='replace')

s_start = text.find('<script>') + 8
e_end = text.rfind('</script>')
script_bytes = data[s_start:e_end]
script_text = text[s_start:e_end]

print('Script bytes: %d, text: %d' % (len(script_bytes), len(script_text)))

showlogin_text = 'function showLogin'
pos = script_text.find(showlogin_text)
print('showLogin at text pos: %d' % pos)

func_bytes = b'function showLogin'
byte_pos = script_bytes.find(func_bytes)
print('showLogin at byte pos: %d' % byte_pos)

if byte_pos > 20:
    before_bytes = script_bytes[byte_pos-20:byte_pos]
    print('Raw before showLogin: %s' % str(before_bytes))
    print('Raw hex: %s' % before_bytes.hex())

# Last 5 lines before showLogin
before = script_text[:pos]
lines = before.split('\n')
print('Last 5 lines before showLogin:')
for line in lines[-5:]:
    print('  %s' % repr(line[-80:]))

print('Char before showLogin: %s (ord=%d)' % (repr(script_text[pos-1]), ord(script_text[pos-1])))
