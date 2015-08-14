@echo off
setlocal enableDelayedExpansion
REM parameters are 1 = Team Project, 2 = Work Item Type, 3 = Collection, 4 = Title, 5 = Assigned To, 6 = Description
set proj=%~1
set type=%~2
set coll=%~3
set coll=!coll: =%%20!
set title=%~4
set user=%~5
set desc=%~6

"C:\Program Files (x86)\Microsoft Team Foundation Server 2013 Power Tools\TFPT.EXE" workitem /new "%proj%"\"%type%" /collection:http://localhost:8080/tfs/%coll% /fields:"Title=%title%;Assigned To=%user%;Description=%desc%"

