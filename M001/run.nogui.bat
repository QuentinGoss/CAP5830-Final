@echo off
REM ~ set python=C:\Users\Leopard\AppData\Local\Programs\Python\Python37\python
set map=..\london-seg4\data\
set veh_total=30
set veh_exists_max=30

:: Nash
python runner.py ^
--nogui ^
--map-dir=%map% ^
--veh.total=%veh_total% ^
--veh.exists.max=%veh_exists_max% ^
--out.dir=out ^
--start=930531404 ^
--poi-file=pois.txt

pause
