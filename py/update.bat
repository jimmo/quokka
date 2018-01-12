
rem -- This is a script for updating your pyboard.
rem -- Note: lines starting with 'rem' are comments in bat files.
rem
rem -- If you've made a change to the quokka libraries or drivers, or
rem -- if this is the first time you've used the pyboard, 
rem -- run update_libraries.bat first.


rem -- update main.py
copy main.py D:\main.py

rem -- The sync command flushes pending writes, to reduce the risk of 
rem -- corrupting the file system on your pyboard.
sync D:\
