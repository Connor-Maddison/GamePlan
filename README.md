# GamePlan
Alternitive / replacement for Pentesting_Quickstart

Originally the plan for Pentesting_Quickstart was to create a tool that could run common commands quickly. Whilst this worked, especially for setting up the reporting Directory and nmap scans, unsurprisingly it was too amitious to try and automate something that tends to be tweaked and customised for each use case.

GamePlan is an alternate approach where it documents some common commands for the attack you want to carry out so you can quickly execute them and find a simple command that you may have forgot that could help. However rather than running the command it outlines some options and you can just copy it into the terminal where you want and tweak as required.

This version also makes use of flags over a CLI so you don't have to navigate a menu but just add the relevent commands for instant results. This also helps make it quicker for repeat use.

These flags also allow for dynamic allocation so rather than a <enter your output directory here> field you can add the directory as an argument and it will dynamically add it into the command for easier copying.
