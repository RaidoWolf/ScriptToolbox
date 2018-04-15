@echo off
color 0A
title Network Admin Access Panel
echo --------------------------
echo ---ADMINISTRATOR ACCESS---
echo --------------------------
echo press [y] to continue
echo press [n] to disconnect
echo --------------------------
echo Currently logged in as: %username%
echo Verification status: unknown
pause >nul
echo Checking user database...
ping 1.1.1.1 -n 1 -w 2000 >nul
echo Database found.
echo Checking DNS server status...
ping 1.1.1.1 -n 1 -w 1250 >nul
echo DNS server found.
echo Validating access...
ping 1.1.1.1 -n 1 -w 3000 >nul
color CF
echo *UNAUTHORIZED ACCESS - [DETECTED]
echo Closing all Local FTP and UDP ports...
ping 1.1.1.1 -n 1 -w 450 >nul
echo Shutdown DNS 192.168.1.1...
ping 1.1.1.1 -n 1 -w 500 >nul
echo Closing all open router points...
ping 1.1.1.1 -n 1 -w 1250 >nul
echo Storing: %username% unauthorized access report...
ping 1.1.1.1 -n 1 -w 350 >nul
echo %username% - unauthorized access report filed.
echo Locking all network connections...
ping 1.1.1.1 -n 1 -w 1000 >nul
color 0A
echo enter password to terminate network closure:
echo PASSWORD:
pause >nul
color CF
echo ACCESS DENIED! Unauthorized user - error 5209A
ping 1.1.1.1 -n 1 -w 750 >nul
color 0A
echo Local network status: 				terminated.
ping 1.1.1.1 -n 1 -w 1500 >nul
echo User database status: 				suspended.
ping 1.1.1.1 -n 1 -w 1500 >nul
echo Administrator account status: 			suspended.
ping 1.1.1.1 -n 1 -w 1500 >nul
echo User account: %username% status:			terminated.
ping 1.1.1.1 -n 1 -w 750 >nul
echo Please contact a network technician.
ping 1.1.1.1 -n 1 -w 2000 >nul
echo Unable to locate Local Network.
ping 1.1.1.1 -n 1 -w 2000 >nul
echo Fatal system error.
ping 1.1.1.1 -n 1 -w 250 >nul
echo Attempting to reconnect...
ping 1.1.1.1 -n 1 -w 2000 >nul
echo Fatal system error.
ping 1.1.1.1 -n 1 -w 250 >nul
echo Attempting to reconnect...
ping 1.1.1.1 -n 1 -w 2000 >nul
echo Fatal system error.
ping 1.1.1.1 -n 1 -w 250 >nul
echo Attempting to reconnect...
ping 1.1.1.1 -n 1 -w 2000 >nul
echo Fatal system error.
ping 1.1.1.1 -n 1 -w 250 >nul
echo Error: User connection not available.
ping 1.1.1.1 -n 1 -w 2000 >nul
echo Closing console.
ping 1.1.1.1 -n 1 -w 3000 >nul
exit