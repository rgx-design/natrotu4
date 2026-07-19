# -*- coding: utf-8 -*-
# Use Playwright to test exactly like a real browser
import subprocess, sys, tempfile, os

# Write a Playwright test script
test_code = '''
const { chromium } = require('playwright');

(async () => {
    const browser = await chromium.launch({ headless: true });
    const context = await browser.newContext();
    const page = await context.newPage();
    
    // Capture ALL console messages
    const logs = [];
    page.on('console', msg => {
        logs.push({ type: msg.type(), text: msg.text(), location: msg.location() });
    });
    
    // Capture errors
    const errors = [];
    page.on('pageerror', err => {
        errors.push(err.message);
    });
    
    // Capture failed requests
    page.on('requestfailed', req => {
        console.log('REQUEST FAILED:', req.url(), req.failure().errorText);
    });
    
    await page.goto('https://natrotu4-production.up.railway.app/', { 
        waitUntil: 'networkidle',
        timeout: 30000
    });
    
    // Wait a bit for scripts to run
    await page.waitForTimeout(3000);
    
    console.log('=== CONSOLE LOGS ===');
    for (const l of logs) {
        console.log('[%s] %s (at %s:%s)' % (l.type, l.text, l.location.url, l.location.lineNumber));
    }
    
    console.log('\\n=== PAGE ERRORS ===');
    for (const e of errors) {
        console.log(e);
    }
    
    // Check if showLogin is defined
    const showLoginType = await page.evaluate(() => typeof showLogin);
    console.log('\\ntypeof showLogin:', showLoginType);
    const showRegisterType = await page.evaluate(() => typeof showRegister);
    console.log('typeof showRegister:', showRegisterType);
    
    // Check the HTML content received
    const html = await page.content();
    console.log('\\nHTML length:', html.length);
    
    // Check if script tag exists and contains showLogin
    const scriptMatch = html.match(/<script>([\\s\\S]*?)<\\/script>/);
    if (scriptMatch) {
        console.log('Script content length:', scriptMatch[1].length);
        console.log('Has function showLogin:', scriptMatch[1].includes('function showLogin'));
        console.log('Has FNCHK:', scriptMatch[1].includes('FNCHK'));
        console.log('Script first 100 chars:', scriptMatch[1].substring(0, 100));
    }
    
    await browser.close();
})();
'''

tmp = tempfile.NamedTemporaryFile(suffix='.js', delete=False, mode='w', encoding='utf-8')
tmp.write(test_code)
tmp.close()
print('Test script:', tmp.name)

result = subprocess.run(
    ['node', tmp.name],
    cwd=r'F:\2fen\natrotu4',
    capture_output=True, text=True, timeout=45
)
print('STDOUT:', result.stdout[:5000])
if result.stderr:
    print('STDERR:', result.stderr[:2000])
print('Return code:', result.returncode)
os.unlink(tmp.name)
