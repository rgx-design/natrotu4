# -*- coding: utf-8 -*-
import urllib.request

url = 'https://natrotu4-production.up.railway.app/'
resp = urllib.request.urlopen(url, timeout=10)
data = resp.read()
text = data.decode('utf-8', errors='replace')

# Find all onclick attributes in the HTML (before the script)
s_start = text.find('<script>')
html_before_script = text[:s_start]

# Find onclick attributes
import re
onclicks = re.findall(r'onclick="([^"]*)"', html_before_script)
print('onclick handlers in HTML:')
for oc in onclicks:
    print('  onclick="%s"' % oc)

# Also check for showLogin reference in the HTML (outside script)
showlogin_refs = re.findall(r'show\w+', html_before_script)
print()
print('showX references in HTML: %s' % set(showlogin_refs))

# Check for login/register button definitions
btn_section = html_before_script[html_before_script.rfind('<body>'):]
print()
print('Last 1000 chars of HTML before script:')
print(repr(btn_section[-1000:]))
