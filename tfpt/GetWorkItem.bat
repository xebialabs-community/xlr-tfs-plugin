@echo off
setlocal enableDelayedExpansion
REM parameters are 1 = Work Item number, 2 = Collection
set num=%~1
set coll=%~2
set coll=!coll: =%%20!

"C:\Program Files (x86)\Microsoft Team Foundation Server 2013 Power Tools\TFPT.EXE" workitem "%num%" /collection:http://localhost:8080/tfs/%coll%

