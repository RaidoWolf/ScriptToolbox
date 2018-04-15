@echo off
title DNS BLOCK - ALTA HIGH SCHOOL
color 0A
echo --------------------------------
echo --------DNS BLOCK - ALTA--------
echo --------------------------------
echo Version 1.0
echo Would you like to block the following sites?
echo www.canyonsdistrict.org, skyward.canyonsdistrict.org
echo altahigh.canyonsdistrict.org
echo PRESS ANY KEY TO BLOCK...
pause >nul
ping 1.1.1.1 -n 1 -w 1500 >nul
echo 127.0.0.1 www.canyonsdistrict.org>>c:\Windows\System32\drivers\etc\hosts
echo BLOCKED: www.canyonsdistrict.org
ping 1.1.1.1 -n 1 -w 1000 >nul
echo 127.0.0.1 skyward.canyonsdistrict.org>>c:\Windows\System32\drivers\etc\hosts
ping 1.1.1.1 -n 1 -w 1000 >nul
echo BLOCKED: skyward.canyonsdistrict.org
ping 1.1.1.1 -n 1 -w 1000 >nul
echo 127.0.0.1 altahigh.canyonsdistrict.org>>c:\Windows\System32\drivers\etc\hosts
echo BLOCKED: skyward.canyonsdistrict.org
ping 1.1.1.1 -n 1 -w 1000 >nul
echo Console will close in 30 seconds...
ping 1.1.1.1 -n 1 -w 30000 >nul
Exit