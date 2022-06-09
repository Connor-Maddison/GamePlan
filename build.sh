#!/bin/bash

###########################################
# Project : GamePlan
# File : build.sh
# Version : 1.0.2

###########################################
# Author : Connor Maddison
# Creation Date : 06/09/2022
# Version Date : 06/09/2022

###########################################


########################################
# Colorcodes
########################################

RED="\033[1;31m"
GREEN="\033[1;32m"
NC="\033[0m"

########################################

if [ "$EUID" -ne 0 ]
    then echo -e $RED"Please run as root$NC"
    exit
else
    sudo cp -r ./GamePlanLibary /usr/local/lib/
    echo -e $GREEN"Moved GamePlanLibary to /usr/local/lib/$NC"
    sudo chmod 755 ./gameplan
    sudo mv -f ./gameplan /usr/local/bin
    echo -e $GREEN"Moved gameplan to /usr/local/bin/$NC"
    sudo rm -r ../GamePlan
fi
