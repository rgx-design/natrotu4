
const fs = require('fs');
const script = fs.readFileSync('F:\\2fen\\natrotu4\\temp_script.js', 'utf8');
// Try to evaluate and check
try {
    // Create a function from the script
    const fn = new Function(script);
    // This won't execute, just parse
    console.log('Script parsed OK');
    // Check syntax more thoroughly
    // We need to extract function declarations
    const showLoginMatch = script.match(/function\s+showLogin/);
    console.log('showLogin function found in source:', !!showLoginMatch);
    if (showLoginMatch) {
        console.log('At position:', showLoginMatch.index);
    }
} catch(e) {
    console.error('Error:', e.message);
}
