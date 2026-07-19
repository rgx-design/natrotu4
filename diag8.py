# -*- coding: utf-8 -*-
import urllib.request, re

resp = urllib.request.urlopen('https://natrotu4-production.up.railway.app/', timeout=10)
data = resp.read()
text = data.decode('utf-8', errors='replace')

s_start = text.find('<script>') + 8
e_end = text.rfind('</script>')
script = text[s_start:e_end]
raw_script = data[s_start:e_end]

# Check for </script> literal in raw bytes
if b'</script' in raw_script:
    idx = raw_script.find(b'</script')
    print('Found </script literal at byte: %d' % idx)
    print('Context: %s' % str(raw_script[idx-30:idx+40]))
else:
    print('No </script literal found')

# Check for unescaped </svg> in raw bytes
if b'</svg>' in raw_script:
    idx = raw_script.find(b'</svg>')
    print('Found unescaped </svg> at byte: %d' % idx)
    print('Context: %s' % str(raw_script[idx-30:idx+30]))

# Check for literal <script in comments (not the opening tag)
# The opening tag was at the start
all_script_starts = [m.start() for m in re.finditer(b'<script', raw_script)]
print('Total <script occurrences in script block: %d' % len(all_script_starts))

# Check the actual HTML buttons - look for showLogin in the HTML
html_part = text[:text.find('<script>')]
# Find all onclick that reference showLogin
onclick_showlogin = re.findall(r'onclick="([^"]*show\w+[^"]*)"', html_part)
print('onclick handlers with showLogin: %s' % onclick_showlogin)

# Most importantly: find EXACTLY what the buttons say
# Find the login/register buttons
btn_area = html_part[html_part.rfind('<body>'):]
print()
print('Last 500 chars before script (HTML buttons area):')
print(repr(btn_area[-500:]))
