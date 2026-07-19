# -*- coding: utf-8 -*-
# Simulate EXACTLY how the browser parses HTML to find the real </script> bug
import urllib.request

resp = urllib.request.urlopen('https://natrotu4-production.up.railway.app/', timeout=10)
data = resp.read()

# Use a simple state machine to parse HTML like a browser
# Browser scans for '<script' then looks for '>' to close the tag
# Then looks for '</script' case-insensitively
script_content_start = None
script_content_end = None
inside_script = False

i = 0
while i < len(data):
    c = chr(data[i]) if data[i] < 128 else '?'
    
    if not inside_script:
        # Look for <script
        if data[i:i+7].lower() == b'<script':
            # Find the '>' that closes this tag
            j = i + 7
            while j < len(data) and data[j] != 62:  # 62 = '>'
                j += 1
            # Now we're past the '>'
            script_content_start = j + 1
            inside_script = True
            i = j + 1
            continue
    else:
        # We're inside script content, look for </script (case insensitive)
        # Browser uses case-insensitive matching for the closing tag
        if data[i:i+9].lower() == b'</script>':
            script_content_end = i
            break
        # Also check for </script followed by any non-letter char
        if data[i:i+9].lower() == b'</script' and i + 9 < len(data):
            next_byte = data[i+9]
            # If next byte is not alphanumeric (like ' ', '>', '/'), it's a closing tag
            if not ((65 <= next_byte <= 90) or (97 <= next_byte <= 122)):
                script_content_end = i
                break
    i += 1

print('Browser parsing result:')
print('  Script content starts at byte: %s' % script_content_start)
print('  Script content ends at byte: %s' % script_content_end)
print('  Script content length: %s' % (script_content_end - script_content_start if script_content_end else 'N/A'))

if script_content_start and script_content_end:
    raw_script = data[script_content_start:script_content_end]
    print()
    print('=== RAW SCRIPT CONTENT (first 300 bytes) ===')
    print(str(raw_script[:300]))
    print()
    print('=== RAW SCRIPT CONTENT (last 100 bytes) ===')
    print(str(raw_script[-100:]))
    print()
    print('=== Check for showLogin function ===')
    print('b"function showLogin" in script: %s' % (b'function showLogin' in raw_script))
    
    # Also check for </script> INSIDE the script content
    bug_positions = [m.start() for m in __import__('re').finditer(r'</script>', raw_script.decode('utf-8', errors='replace'))]
    if bug_positions:
        print()
        print('!!! BUG FOUND: </script> inside script at positions: %s' % bug_positions)
        for pos in bug_positions:
            print('  Context: %s' % repr(raw_script[max(0,pos-50):pos+20]))
