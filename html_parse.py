# -*- coding: utf-8 -*-
import urllib.request, re

resp = urllib.request.urlopen('https://natrotu4-production.up.railway.app/', timeout=10)
data = resp.read()
text = data.decode('utf-8', errors='replace')

# Check for style tags - HTML parser would look for </style>
style_opens = [m.start() for m in re.finditer(r'<style', text)]
style_closes = [m.start() for m in re.finditer(r'</style>', text)]
print('Style tags: opens at %s, closes at %s' % (style_opens, style_closes))

# Check if all style tags are properly closed
if len(style_opens) != len(style_closes):
    print('MISMATCH: %d <style> vs %d </style>' % (len(style_opens), len(style_closes)))
    # Find which ones are unclosed
    for i, pos in enumerate(style_opens):
        # Find corresponding close
        corresponding_close = None
        for cpos in style_closes:
            if cpos > pos:
                corresponding_close = cpos
                break
        if not corresponding_close:
            print('  <style> at %d has no close!' % pos)
            # Show content after this unclosed style
            chunk = text[pos:pos+200]
            print('  Content: %s' % repr(chunk[:200]))
        else:
            if i < len(style_closes):
                print('  <style>[%d] closed by </style>[%d] at %d' % (i, i, corresponding_close))

# Check for textarea, pre, template tags (also suppress script detection)
for tag in ['<textarea', '<pre', '<template', '<xmp', '<listing']:
    opens = [m.start() for m in re.finditer(re.escape(tag), text)]
    closes = [m.start() for m in re.finditer(tag.replace('<', '</'), text)]
    if opens:
        print('%s: %d opens, %d closes' % (tag, len(opens), len(closes)))

# Find the ACTUAL position of the first </script> tag in the RAW bytes
# (not the script content, but the actual HTML tag)
script_tag = b'</script>'
positions = [m.start() for m in re.finditer(r'</script>', text)]
print()
print('All </script> occurrences in text: %s' % positions)

# Also check: where does the FIRST real </script> HTML tag appear?
# vs where does the script CONTENT end?
first_script_close_text = text.find('</script>')
first_script_open_text = text.find('<script>')
print()
print('First <script> in text: %d' % first_script_open_text)
print('First </script> in text: %d' % first_script_close_text)

# Check raw bytes around the first </script>
raw_first_close = data.find(b'</script>')
print('First </script> in raw bytes: %d' % raw_first_close)
print('Raw bytes around it: %s' % str(data[raw_first_close-5:raw_first_close+20]))

# Count occurrences
print('Total </script> in text: %d' % text.count('</script>'))
print('Total </script> in raw bytes: %d' % data.count(b'</script>'))

# Find ALL script element positions (open and close)
print()
print('All <script> positions: %s' % [m.start() for m in re.finditer(r'<script>', text)])
print('All </script> positions: %s' % [m.start() for m in re.finditer(r'</script>', text)])
