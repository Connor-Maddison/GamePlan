#!/bin/bash

###########################################
# Project : GamePlan
# File : gameplan.sh
# Version : 1.0.0

###########################################
# Author : Connor Maddison
# Creation Date : 05/29/2022
# Version Date : 05/29/2022

###########################################



########################################
# Colorcodes
########################################

RED="\033[1;31m"
GREEN="\033[1;32m"
BLUE="\033[1;34m"
DARKGREY="\033[1;90m" 
NC="\033[0m"

########################################


Banner()
{
echo -e $DARKGREY"- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

.------..------..------..------.     .------..------..------..------.
|"$BLUE"G$DARKGREY.--. ||"$BLUE"A$DARKGREY.--. ||"$BLUE"M$DARKGREY.--. ||"$BLUE"E$DARKGREY.--. |.-.  |"$BLUE"P$DARKGREY.--. ||"$BLUE"L$DARKGREY.--. ||"$BLUE"A$DARKGREY.--. ||"$BLUE"N$DARKGREY.--. |
| :/\: || (\/) || (\/) || (\/) ((1)) | :/\: || :/\: || (\/) || :(): |
| :\/: || :\/: || :\/: || :\/: |'-.-.| (__) || (__) || :\/: || ()() |
| '--'"$BLUE"G$DARKGREY|| '--'"$BLUE"A$DARKGREY|| '--'"$BLUE"M$DARKGREY|| '--'"$BLUE"E$DARKGREY| ((1)) '--'"$BLUE"P$DARKGREY|| '--'"$BLUE"L$DARKGREY|| '--'"$BLUE"A$DARKGREY|| '--'"$BLUE"N$DARKGREY|
\`------'\`------'\`------'\`------'  '-'\`------'\`------'\`------'\`------'
$BLUE
   ______                              _______  __                   
 .' ___  |                            |_   __ \[  |                  
/ .'   \_|  ,--.   _ .--..--.  .---.    | |__) || |  ,--.   _ .--.   
| |   ____ \`'_\ : [ \`.-. .-. |/ /__\\\\\   |  ___/ | | \`'_\ : [ \`.-. | 
\ \`.___]  |// | |, | | | | | || \__.,  _| |_    | | // | |, | | | |  
 \`._____.' \'-;__/[___||__||__]'.__.' |_____|  [___]\'-;__/[___||__] 
 
 
$DARKGREY- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -$NC"
}

usage()
{
########################################
# Explain how to use
########################################

file="./usage.txt"
while read -r line
do
	echo -e "$line"
done < "$file"

}

YesNo()
{
########################################
# Call to pose a yes no option
########################################
#arg 1 = Question

question=$(echo $1)
accept=false
	
#loop untill a acceptable option is selected
#echo to >&2 (error) so value isnt returned
while [ $accept == false ]
do
	echo -e $DARKGREY"- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -$NC" >&2
	echo -e $BLUE"$question"$NC >&2
	echo -e $GREEN"[0]$NC - No" >&2
	echo -e $RED"[1]$NC - Yes" >&2
	echo -e $DARKGREY"- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -$NC" >&2
	read responce
	

	if [ $responce == 0 ] 
	then
		accept=true
		answer=false
	elif [ $responce == 1 ]
	then
		accept=true	
		answer=true
	else
		echo -e $RED"Incorrect Input"$NC >&2
	fi
done

echo $answer
	
}

createDir()
{
########################################
# Create Reporting Directory
########################################

	#Ask what folders to create
	webFolder=$(YesNo "Create web folder?")
	hashFolder=$(YesNo "Create hashes folder?")
	exploitFolder=$(YesNo "Create exploit folder?")
	imageFolder=$(YesNo "Create image folder?")
	bruteFolder=$(YesNo "Create bruteforce folder?")
	
	#Ask the directory names to an array for later
	folders=("report" "nmap_scans")
	
	if [ $webFolder == true ]
	then
		folders+=("web")
	fi
	if [ $hashFolder == true ]
	then
		folders+=("hashes")
	fi
	if [ $exploitFolder == true ]
	then
		folders+=("exploits")
	fi
	if [ $imageFolder == true ]
	then
		folders+=("images")
	fi
	if [ $bruteFolder == true ]
	then
		folders+=("bruteforce")
	fi
	
	#create a string copy to show to user for them to accept
	foldersMsg=$(echo ${folders[@]})
	
	#make sure user is happy with location and folders before creating
	accepted=$(YesNo "Create reporting directory: $create$NC\nIn location $DARKGREY$directory/$BLUE$create$NC\nWith the following folders:$BLUE\n$foldersMsg")
	
	#If they accept create the actuakl folders
	if [ $accepted == true ]
	then
		echo -e $DARKGREY"- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -$NC" 
		echo -e $BLUE"Creating reporting directory"$NC 
		for dir in ${folders[@]}
		do
			mkdir -p $directory/$create/$dir
			echo -e "Created directory :$DARKGREY$directory/$create/$BLUE$dir$NC"
		done
		
		#create the reporting text file
		
echo "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Pentest of : $target 
Date : $(date +"%h %d %Y")
Time : $(date +"%H:%M:%S")
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
" >> "$directory/$create/report/report.txt"
		 
	else
		exit 0
	fi

}

readCommands()
{
########################################
# Display chosen attack commands
########################################
#arg 1 = file location

ID=$(date +"%h_%d_%H%M%S") # unique identifier for output file
file=$1
while read -r line
do	
	#Add the arguments from command to the comments in file
	addArgs=$(echo ${line//'$target'/"$target"})
	addArgs=$(echo ${addArgs//'$directory'/"$directory"})
	addArgs=$(echo ${addArgs//'$ID'/"$ID"})
	addArgs=$(echo ${addArgs//'$wordlist'/"$wordlist"})
	echo -e $addArgs
done < "$file"
}

Attacks()
{
########################################
# Display correct commands based on choice
########################################

#if chosen web show web commands
if [ $attack == "web" ]
then
	#Requires a target atleast
	if [ -z $target ]
	then 
		echo -e "$0 ${@/"web"/$RED"web$NC"}" #outline the web tag which requires a target
		echo -e $RED"Target tag (-t) required"$NC
		exit 126
	fi
	if [ -z $directory ]
	then 
		directory="<enter output directory>"
	fi
	if [ -z $wordlist ]
	then 
		wordlist="<enter wordlist directory>"
	fi
	readCommands "./webcommands.txt"
	exit 0

#if chosen image show image commands
elif [ $attack == "image" ]
then
	#Requires a target atleast
	if [ -z $target ]
	then 
		echo -e "$0 ${@/"image"/$RED"image$NC"}" #outline the image tag which requires a target
		echo -e $RED"Target tag (-t) required"$NC
		exit 126
	fi
	if [ -z $directory ]
	then 
		directory="<enter output directory>"
	fi
	if [ -z $wordlist ]
	then 
		wordlist="<enter wordlist directory>"
	fi
	readCommands "./imagecommands.txt"
	exit 0
fi

}



Banner  

while getopts h:c:d:t:a:w: flag
do
    case "${flag}" in
    	h) usage; exit 2;;
        c) create=${OPTARG};; # create a report with name provided
        d) directory=${OPTARG};; # create a report at location provided
        t) target=${OPTARG};; # target ip
        a) attack=${OPTARG};; # Show web attacks
        w) wordlist=${OPTARG};;
        *) echo -e $RED"Incorrect usage"$NC; usage; exit 2;;
    esac
done


#create a reporting / project directory
if [[ ! -z $create ]]
then 
	
	#make sure there is a directory tag
	if [ -z $directory ]
	then 
		echo -e $RED"Directory tag (-d) required to create a reporing directory"$NC
		exit 126
	fi
	echo -e $BLUE"Creating Reporting Directory for project $create"$NC
	createDir
	exit 0
	
fi

#make sure correct attack is entered
if [ $attack == "image" ] || [ $attack == "web" ]
then
	Attacks $@
	exit 0
else
	echo -e $RED"Incorrect attack entered"$NC
	usage
	exit 2
	
fi
