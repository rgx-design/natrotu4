# -*- coding: utf-8 -*-
import urllib.request

url = 'https://natrotu4-production.up.railway.app/'
resp = urllib.request.urlopen(url, timeout=10)
data = resp.read()
text = data.decode('utf-8', errors='replace')

s_start = text.find('<script>') + 8
e_end = text.rfind('</script>')
script = text[s_start:e_end]

# Error is at char 11898 (relative to script content)
pos = 11898
print('Around error pos %d:' % pos)
print(repr(script[pos-100:pos+100]))
print()

# Also check: what is the TOTAL script length?
print('Script length: %d' % len(script))
print('Error position is at %.1f%% of script' % (pos * 100.0 / len(script)))

# Find the function containing pos 11898
# Look backwards for 'function ' or 'async function '
chunk_before = script[:pos]
funcs_found = [(m.start(), m.group()) for m in __import__('re').finditer(r'(?:async\s+)?function\s+\w+', chunk_before)]
if funcs_found:
    last_func = funcs_found[-1]
    print('Last function defined before pos %d: %s at %d' % (pos, last_func[1], last_func[0]))
    print('Context: %s' % repr(script[last_func[0]:last_func[0]+80]))

# Now look at the actual variable reference near pos 11898
# The error is likely an undefined variable used in an expression
# Check what's on the line containing pos 11898
# Find the line containing pos 11898
lines_up_to = script[:pos].split('\n')
current_line_num = len(lines_up_to)
current_line = lines_up_to[-1]
print()
print('Line %d: %s' % (current_line_num, repr(current_line)))
print('Line %d+1: %s' % (current_line_num, repr(script[pos:pos+100].split('\n')[0])))

# Try to find undefined variable patterns: word followed by ( or . or = without let/const/var
import re
# Look for patterns like 'word(' or 'word.' or 'word =' that might be undefined
nearby = script[max(0,pos-200):pos+200]
# Find identifiers followed by ( that aren't known functions
known_funcs = {'console', 'fetch', 'Array', 'JSON', 'Object', 'window', 'document', 
               'showLogin', 'showRegister', 'login', 'register', 'logout', 'submitLogin',
               'submitRegister', 'updateNavbar', 'showLoading', 'hideLoading', 'showError',
               'saveUserData', 'loadUserData', 'saveUserProgress', 'loadUserProgress',
               'getCurrentUser', 'checkAnswer', 'nextWord', 'loadGame', 'updateScore',
               'saveScore', 'loadScore', 'showGameOver', 'renderLeaderboard',
               'renderWrongWords', 'showWrongWords', 'fetchLeaderboard', 'clearError',
               'showSuccess', 'Math', 'Date', 'Promise', 'setTimeout', 'setInterval',
               'alert', 'confirm', 'prompt', 'parseInt', 'parseFloat', 'isNaN', 'isFinite',
               'encodeURIComponent', 'decodeURIComponent', 'btoa', 'atob', 'open', 'close',
               'getElementById', 'querySelector', 'querySelectorAll', 'addEventListener',
               'removeEventListener', 'preventDefault', 'stopPropagation', 'push', 'pop',
               'shift', 'unshift', 'slice', 'splice', 'map', 'filter', 'reduce', 'forEach',
               'includes', 'indexOf', 'match', 'replace', 'split', 'trim', 'length', 'innerHTML',
               'textContent', 'style', 'classList', 'getAttribute', 'setAttribute', 'hasAttribute'}
idents = re.findall(r'\b([a-zA-Z_$][a-zA-Z0-9_$]*)\s*\(', nearby)
unknown = [i for i in idents if i not in known_funcs]
print()
print('Function calls near error (unknown functions): %s' % unknown)
