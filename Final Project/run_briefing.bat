@echo off
REM Daily Assistant Agent - Automated Briefing
REM This script runs the briefing pipeline daily

cd /d "C:\Users\mong3\Documents\GitHub\oim3640\Final Project"
python main.py

REM Log the execution
echo Briefing ran at %date% %time% >> briefing_log.txt
