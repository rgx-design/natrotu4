# Read the first 200 chars of the script section
content = open(r'F:\2fen\natrotu4\index.html', 'r', encoding='utf-8').read()
script_start = content.find('<script>') + 8
print('Script starts at char: %d' % script_start)
print('First 200 chars of script:')
print(repr(content[script_start:script_start+200]))
