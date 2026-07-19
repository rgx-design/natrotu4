# -*- coding: utf-8 -*-
import urllib.request

resp = urllib.request.urlopen('https://natrotu4-production.up.railway.app/', timeout=10)
data = resp.read()
text = data.decode('utf-8', errors='replace')

# Find the script section
script_open = text.find('<script>') + 8
script_close = text.rfind('</script>')
script = text[script_open:script_close]

# Show first 200 chars
print('=== SCRIPT FIRST 200 CHARS ===')
print(repr(script[:200]))
print()

# CRITICAL: Find ALL </script> occurrences WITHIN the script content
# (Not counting the HTML closing tag)
import re
all_closes = [(m.start(), m.group()) for m in re.finditer(r'</script>', script)]
print('All </script> occurrences in script:')
for pos, tag in all_closes:
    print('  At char %d: %s' % (pos, repr(script[max(0,pos-30):pos+30])))
print()

# Also check for </SCRIPT> (case variations)
for variant in ['</SCRIPT>', '</Script>', '</sCRIPT>', '</scRIPT>', '</scrIPT>', '</scrIPT>', '</scriPT>', '</sCript>']:
    count = script.count(variant)
    if count:
        print('Found %s: %d times' % (variant, count))

# Also check raw bytes for any embedded </script> pattern
raw_script = data[script_open:script_close]
script_close_tag = b'</script>'
positions = [m.start() for m in re.finditer(r'</script>', raw_script.decode('utf-8', errors='replace'))]
print()
print('All </script> in script (text): %s' % positions)
raw_positions = [m.start() for m in re.finditer(b'</script>', raw_script)]
print('All </script> in script (bytes): %s' % raw_positions)

# Most critical: check if the function showLogin() {} exists in the script
# using raw bytes (not decoded text)
print()
print('=== FUNCTION showLogin CHECK ===')
print('In script text: %s' % ('function showLogin' in script))
print('In raw bytes: %s' % (b'function showLogin' in raw_script))

# Show what the raw bytes look like around "function showLogin"
if b'function showLogin' in raw_script:
    pos = raw_script.find(b'function showLogin')
    print('Raw bytes around showLogin:')
    print(str(raw_script[pos-10:pos+80]))
    print('Hex: %s' % raw_script[pos-10:pos+80].hex())
