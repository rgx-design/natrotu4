# -*- coding: utf-8 -*-
import urllib.request

url = 'https://natrotu4-production.up.railway.app/'
resp = urllib.request.urlopen(url, timeout=10)
data = resp.read()
text = data.decode('utf-8', errors='replace')

s_start = text.find('<script>') + 8
e_end = text.rfind('</script>')
script = text[s_start:e_end]

# Show the exact area around char 492
print('=== Around char 492 (unclosed string) ===')
print(repr(script[460:540]))
print()
print('=== Around char 1-100 ===')
print(repr(script[:100]))
