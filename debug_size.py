# -*- coding: utf-8 -*-
with open(r'F:\2fen\natrotu4\index.html', 'rb') as f:
    data = f.read()
print('File size: %d' % len(data))

text = data.decode('utf-8', errors='replace')
body_pos = text.find('<body>')
print('First <body> at: %d' % body_pos)

body_end = body_pos + 6
print('body_end = %d' % body_end)
print('text[:body_end] length: %d' % len(text[:body_end]))
print('text[:body_end]: %s' % repr(text[:body_end]))

banner = '<div id="v552banner" style="background:#cc0000;color:#fff">v552</div>'
print('Banner length: %d' % len(banner))
print('Banner: %s' % repr(banner))

result = text[:body_end] + banner + text[body_end:]
print('Result length: %d' % len(result))
print('Expected: %d + %d + %d = %d' % (body_end, len(banner), len(text)-body_end, body_end+len(banner)+len(text)-body_end))
