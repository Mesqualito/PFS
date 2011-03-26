@echo off

if %1!==! goto usage

set PYTHON=C:\Python27\python.exe

if "%1"=="compile" goto compile
if "%1"=="clean" goto clean
if "%1"=="package" goto package
goto end

:compile
%PYTHON% setup.py build
goto end

:clean
%PYTHON% setup.py Clean
goto end

:package
%PYTHON% setup.py bdist_win bdist_wininst
goto end


:usage
echo usage:
echo   make clean
echo   make compile
echo   make package

:end
