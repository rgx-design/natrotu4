# -*- coding: utf-8 -*-
import urllib.request, re

url = 'https://natrotu4-production.up.railway.app/'
resp = urllib.request.urlopen(url, timeout=10)
data = resp.read()

text = data.decode('utf-8', errors='replace')
s_start = text.find('<script>') + 8
e_end = text.rfind('</script>')
script = text[s_start:e_end]

# Find fetchLeaderboard function
fl_pos = script.find('async function fetchLeaderboard')
if fl_pos < 0:
    fl_pos = script.find('function fetchLeaderboard')
print('fetchLeaderboard at: %d' % fl_pos)

# Print the full function
print()
print('=== fetchLeaderboard function ===')
# Find the function body
fn_start = script.find('{', fl_pos)
# Count braces to find matching close
depth = 0
fn_end = fn_start
for i in range(fn_start, len(script)):
    if script[i] == '{':
        depth += 1
    elif script[i] == '}':
        depth -= 1
        if depth == 0:
            fn_end = i + 1
            break

fn_body = script[fl_pos:fn_end]
print(fn_body[:500])
print('...')
print(fn_body[-100:])

# Check for undeclared variables (look for = without let/const/var/function)
# Common pattern: using a variable without declaring it
# Let's check what variables are used in this function
print()
print('=== Variables in fetchLeaderboard ===')
# Extract all identifiers
identifiers = re.findall(r'[a-zA-Z_$][a-zA-Z0-9_$]*', fn_body)
unique_ids = sorted(set(identifiers))
print(str(unique_ids))

# Check which of these are likely undeclared:
# window, document, console, Array, JSON, fetch, Response, Error, Promise are globals
# Let's check what might be undefined
global_names = {'window', 'document', 'console', 'Array', 'Object', 'JSON', 'fetch', 
                'Promise', 'Error', 'TypeError', 'response', 'data', 'type', 'limit',
                'url', 'result', 'r', 'i', 'j', 'k', 'str', 'val', 'key', 'item',
                'Boolean', 'Number', 'String', 'Math', 'Date', 'RegExp', 'Map', 'Set',
                'URLSearchParams', 'Headers', 'Request'}
# Not global but defined elsewhere in the script:
defined_elsewhere = {'showLogin', 'showRegister', 'login', 'register', 'logout', 'submitLogin',
                     'submitRegister', 'switchToRegister', 'switchToLogin', 'checkAuth',
                     'updateNavbar', 'showLoading', 'hideLoading', 'showError', 'showSuccess',
                     'clearError', 'saveUserData', 'loadUserData', 'saveUserProgress',
                     'loadUserProgress', 'getCurrentUser', 'checkAnswer', 'nextWord',
                     'loadGame', 'updateScore', 'saveScore', 'loadScore', 'showGameOver',
                     'renderLeaderboard', 'renderWrongWords', 'showWrongWords',
                     'fetchLeaderboard', 'currentUser', 'authToken', 'API_BASE',
                     'username', 'password', 'email', 'gameState', 'words', 'currentWordIndex',
                     'correctCount', 'wrongCount', 'score', 'timer', 'hardMode', 'wrongWords',
                     'totalScore', 'todayScore', 'gameMode', 'difficulty'}

potentially_undeclared = [i for i in unique_ids if i not in global_names and i not in defined_elsewhere]
print('Potentially undeclared: %s' % str(potentially_undeclared))
