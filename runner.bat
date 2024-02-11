@echo off

REM Start destination first
start python destination\destination.py

REM Give the destination some time to start up (adjust the timeout as needed)
timeout /t 3

REM Start the router
start python router\router.py

REM Give the router some time to start up (adjust the timeout as needed)
timeout /t 2

REM Start the client
start python client\client.py