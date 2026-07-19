# -*- coding: utf-8 -*-
# Create a patched index.html with extra diagnostics
content = open(r'F:\2fen\natrotu4\index.html', 'r', encoding='utf-8').read()
script_start = content.find('<script>') + 8
script_end = content.rfind('</script>')

# Find showLogin function definition
showlogin_def = content.find('function showLogin()', script_start)
print('showLogin at char: %d' % showlogin_def)

# Find end of showLogin function (next function or end of script)
# Look for the next "function " after showLogin
next_func = content.find('function ', showlogin_def + 20)
print('Next function at char: %d' % next_func)

# The showLogin function body is between showlogin_def and next_func
showlogin_body = content[showlogin_def:next_func]
print('showLogin body preview:')
print(repr(showlogin_body[:200]))

# PATCH: Add a diagnostic call right after showLogin is defined
# We'll insert "window.__debugShowLogin = showLogin;" right after showLogin function
showlogin_end = next_func
# The showLogin function ends with "}" and then next function starts
# Find the exact end of showLogin (its closing brace)
# showLogin body ends with "}" 
showlogin_body_content = content[showlogin_def:showlogin_end]
print()
print('Full showLogin body (last 100 chars):')
print(repr(showlogin_body_content[-100:]))

# Add diagnostic: insert console.log right after showLogin function definition
# This will fire IMMEDIATELY after showLogin is defined
patch_content = (
    content[:showlogin_end] +
    '\nwindow.__testSL=typeof showLogin;' +
    content[showlogin_end:]
)

# Also update the DEBUG version number so we can confirm the new script is loaded
patch_content = patch_content.replace(
    'console.log("[DEBUG] Script tag found, version: 548");',
    'console.log("[DEBUG] Script tag found, version: 549 - showLogin type:", typeof showLogin);'
)

print()
print('=== PATCH RESULT ===')
print('Old DEBUG line:')
print(repr(content[script_start:script_start+100]))
print('New DEBUG line:')
new_script_start = patch_content.find('<script>') + 8
print(repr(patch_content[new_script_start:new_script_start+120]))

# Write the patched file
with open(r'F:\2fen\natrotu4\index_new.html', 'w', encoding='utf-8') as f:
    f.write(patch_content)
print()
print('Written to index_new.html')
