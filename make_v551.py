# -*- coding: utf-8 -*-
# Create the v551 diagnostic version
# Strategy: replace the DEBUG line with a comprehensive function definition check
# that runs IMMEDIATELY after each function is declared
content = open(r'F:\2fen\natrotu4\index.html', 'r', encoding='utf-8').read()
script_start = content.find('<script>') + 8
script_end = content.rfind('</script>')

# Replace the simple DEBUG line with comprehensive diagnostics
# Insert checks after each function is declared
old_debug = 'console.log("[DEBUG] Script tag found, version: 548");'

# Create new diagnostic that runs at the END of all function definitions
# and at the START of initialization
new_diagnostic = '''console.log("[DEBUG] Script tag found, version: 551 - structure check:");
window.__fnCheck=()=>{console.log("FNCHK","showLogin="+typeof showLogin,"hideLogin="+typeof hideLogin,"showRegister="+typeof showRegister,"doLogin="+typeof doLogin,"updateHeaderAuth="+typeof updateHeaderAuth,"renderRank="+typeof renderRank);};
window.__fnCheck();
// Run again after a brief delay to catch any async issues
setTimeout(()=>{console.log("FNCHK-DELAYED","showLogin="+typeof showLogin);},100);'''

patched = content.replace(old_debug, new_diagnostic)

# Also change the DOMContentLoaded to add more diagnostics
old_domready = "document.addEventListener('DOMContentLoaded', async () => {"
new_domready = '''document.addEventListener('DOMContentLoaded', async () => {
            console.log("[DEBUG] DOMContentLoaded fired");
            window.__fnCheck();'''
patched = patched.replace(old_domready, new_domready)

# Verify the patch was applied
if new_diagnostic in patched:
    print('Patch applied successfully')
    print('New DEBUG content:')
    s = patched.find('[DEBUG]')
    print(repr(patched[s:s+200]))
else:
    print('ERROR: patch not applied!')
    print('Looking for old debug:')
    print(repr(content[script_start:script_start+100]))

# Write the new file
with open(r'F:\2fen\natrotu4\index.html', 'w', encoding='utf-8') as f:
    f.write(patched)
print()
print('Written to index.html')
