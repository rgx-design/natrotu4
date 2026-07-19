# -*- coding: utf-8 -*-
# Find ALL occurrences of showLogin in the local file
content_local = open(r'F:\2fen\natrotu4\index.html', 'r', encoding='utf-8').read()
script_start = content_local.find('<script>') + 8
script_end = content_local.rfind('</script>')

# Find all showLogin references
import re
for m in re.finditer(r'showLogin', content_local):
    pos = m.start()
    in_script = script_start <= pos < script_end
    print('showLogin at char %d [%s]: %s' % (pos, 'SCRIPT' if in_script else 'HTML', repr(content_local[max(0,pos-30):pos+60])))

print()
print('Total showLogin occurrences: %d' % len(re.findall(r'showLogin', content_local)))
print()

# Also find all function declarations
funcs = [(m.start(), m.group(1)) for m in re.finditer(r'function\s+(\w+)\s*\(', content_local)]
print('All function declarations in LOCAL file:')
for pos, name in funcs:
    in_script = script_start <= pos < script_end
    print('  %s at char %d [%s]' % (name, pos, 'SCRIPT' if in_script else 'HTML'))
