@echo off
echo ===================================
echo WeyFusion GitHub Push Tool
echo ===================================
echo:

python push_to_github.py %*

echo:
echo Press any key to exit...
pause > nul 