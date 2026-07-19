# -*- coding: utf-8 -*-
import urllib.request

resp = urllib.request.urlopen('https://natrotu4-production.up.railway.app/', timeout=10)
data = resp.read()
text = data.decode('utf-8', errors='replace')

# Check the EXACT bytes around <script> tag
script_open_pos_bytes = data.find(b'<script>')
print('First <script> at byte: %d' % script_open_pos_bytes)
print('Bytes around it: %s' % str(data[script_open_pos_bytes-10:script_open_pos_bytes+20]))
print('Hex: %s' % data[script_open_pos_bytes-10:script_open_pos_bytes+20].hex())

# Also check: does the HTML have any content between </style> and <script>?
style_close = data.find(b'</style>')
script_open = data.find(b'<script>')
between = data[style_close:script_open]
print()
print('Bytes between </style> and <script>: %d bytes' % len(between))
print('Content (repr): %s' % repr(between[:200]))

# Most important: what's the EXACT content of the <script> tag attributes?
# (Check for any type="module" or other attributes that change behavior)
# Find the <script> tag in the raw HTML
script_tag_start = data.find(b'<script>')
script_tag_end = data.find(b'>', script_tag_start)
print()
print('Full <script> tag: %s' % str(data[script_tag_start:script_tag_end+1]))
