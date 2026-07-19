# -*- coding: utf-8 -*-
import urllib.request

# Compare local vs Railway
url = 'https://natrotu4-production.up.railway.app/'
resp = urllib.request.urlopen(url, timeout=10)
railway_data = resp.read()
railway_text = railway_data.decode('utf-8', errors='replace')

with open(r'F:\2fen\natrotu4\index.html', 'rb') as f:
    local_data = f.read()
local_text = local_data.decode('utf-8', errors='replace')

print('Local file: %d bytes, Railway HTML: %d bytes' % (len(local_data), len(railway_data)))

# Extract scripts
rs = railway_text.find('<script>') + 8
re_end = railway_text.rfind('</script>')
railway_script = railway_text[rs:re_end]
railway_script_raw = railway_data[rs:re_end]

ls = local_text.find('<script>') + 8
le_end = local_text.rfind('</script>')
local_script = local_text[ls:le_end]

print('Local script: %d chars, Railway script: %d chars' % (len(local_script), len(railway_script)))
print('Local script raw: %d bytes, Railway script raw: %d bytes' % (len(local_data) - len('<script>'), len(railway_script_raw)))

# Check: what's the extra bytes in Railway?
if len(railway_script_raw) > len(local_script.encode('utf-8')):
    print()
    print('RAILWAY HAS MORE BYTES! Difference: %d' % (len(railway_script_raw) - len(local_script.encode('utf-8'))))
    # Find where first difference is
    min_len = min(len(local_script), len(railway_script_raw))
    for i in range(min_len):
        if local_script.encode('utf-8')[i:i+1] != railway_script_raw[i:i+1]:
            print('First diff at char %d:' % i)
            print('  Local:   %s' % str(local_script.encode('utf-8')[max(0,i-20):i+40]))
            print('  Railway: %s' % str(railway_script_raw[max(0,i-20):i+40]))
            break

# Check the beginning and end of Railway script
print()
print('Railway script first 100 chars:')
print(repr(railway_script[:100]))
print()
print('Railway script last 100 chars:')
print(repr(railway_script[-100:]))

# Find GBK-like bytes in Railway script raw
print()
print('Checking for GBK/encoding issues in Railway script...')
gbk_issues = 0
for i in range(len(railway_script_raw)):
    b = railway_script_raw[i]
    # Check for GBK lead bytes (0x81-0xFE) followed by trail byte (0x40-0xFE)
    if 0x81 <= b <= 0xFE:
        if i + 1 < len(railway_script_raw):
            nb = railway_script_raw[i+1]
            if 0x40 <= nb <= 0xFE or 0x80 <= nb <= 0xFE:
                gbk_issues += 1
                if gbk_issues <= 5:
                    print('  Possible GBK at byte %d: %s' % (i, str(railway_script_raw[i:i+2])))
print('Total possible GBK sequences: %d' % gbk_issues)
