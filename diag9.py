# -*- coding: utf-8 -*-
import urllib.request, re

resp = urllib.request.urlopen('https://natrotu4-production.up.railway.app/', timeout=10)
data = resp.read()
text = data.decode('utf-8', errors='replace')

s_start = text.find('<script>') + 8
e_end = text.rfind('</script>')
script = text[s_start:e_end]

# Find the LAST function defined in the script
funcs = list(re.finditer(r'function\s+(\w+)\s*\(', script))
print('Last 5 functions:')
for m in funcs[-5:]:
    print('  %s at char %d: %s' % (m.group(1), m.start(), repr(script[m.start():m.start()+80])))

# Find renderMarquee and showRank - these are at the END of the script
rm_pos = script.find('function renderMarquee')
sr_pos = script.find('function showRank')
print()
print('renderMarquee: %d, showRank: %d, script end: %d' % (rm_pos, sr_pos, len(script)))
print('Space between renderMarquee and showRank: %d' % (sr_pos - rm_pos - len('function renderMarquee() {}')))

# Look at the LAST 500 chars of the script
print()
print('=== LAST 500 chars of script ===')
print(repr(script[-500:]))
print()

# Check: what runs AFTER the function definitions? 
# Look for any code after the last function that's NOT in a function
after_last_func = script[funcs[-1].end():]
print('=== After last function (%s) ===' % funcs[-1].group(1))
print(repr(after_last_func[:300]))
