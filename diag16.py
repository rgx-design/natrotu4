# -*- coding: utf-8 -*-
import urllib.request, re

resp = urllib.request.urlopen('https://natrotu4-production.up.railway.app/', timeout=10)
data = resp.read()
text = data.decode('utf-8', errors='replace')

print('Content length: %d' % len(data))

script_open = text.find('<script>') + 8
script_close = text.rfind('</script>')
script = text[script_open:script_close]

# Check version
if 'version: 551' in script:
    print('v551 DETECTED')
elif 'version: 548' in script:
    print('v548 DETECTED (OLD)')
else:
    print('UNKNOWN VERSION')

# Check for </script> in script content
if '</script>' in script:
    print('BUG: </script> FOUND in script content')
else:
    print('OK: no </script> in script content')

# Check for unescaped </script> anywhere in HTML
# The browser parses HTML from top to bottom - any </script> before the actual close is a bug
all_closes = [m.start() for m in re.finditer(r'</script>', text)]
print()
print('Total </script> in full HTML: %d' % len(all_closes))
for pos in all_closes:
    context = text[max(0, pos-40):pos+9]
    print('  At %d: %s' % (pos, repr(context)))
