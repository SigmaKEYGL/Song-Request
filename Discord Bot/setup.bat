@echo off
title Python Package Installer
color 0A

echo ==================================================
echo          Python Package Installer Script
echo ==================================================
echo.
echo This script will install the following Python packages:
echo  - discord
echo  - asyncio
echo  - yt_dlp
echo  - google-api-python-client
echo.
echo Press any key to start the installation process...
pause >nul

echo.
echo ==================================================
echo Installing packages...
echo ==================================================

pip install discord
pip install asyncio
pip install yt_dlp
pip install google-api-python-client

echo.
echo ==================================================
echo All packages have been installed successfully!
echo ==================================================
pause
