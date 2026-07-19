@echo off
cd /d F:\2fen\natrotu4
git add server-test.js
git commit -m "fix: add no-cache headers for HTML to prevent browser serving stale cached version"
git push origin main
