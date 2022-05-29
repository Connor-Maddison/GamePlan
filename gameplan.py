#!/usr/bin/env python3

###########################################
# Project : GamePlan
# File : gameplan.py
# Version : 2.0.0

###########################################
# Author : Connor Maddison
# Creation Date : 05/29/2022
# Version Date : 05/29/2022

###########################################

import argparse, os, datetime, csv, time

########################################
# Colorcodes
########################################

RED="\033[1;31m"
GREEN="\033[1;32m"
BLUE="\033[1;34m"
DARKGREY="\033[1;90m" 
NC="\033[0m"
BOLD="\033[1m"

########################################
# arguments
########################################

directory=""
target=""
create=""
wordlist=""
search=""
tags=False

########################################

def Banner():
    print( DARKGREY+"""- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

.------..------..------..------.     .------..------..------..------.
|"""+BLUE+"""G"""+DARKGREY+""".--. ||"""+BLUE+"""A"""+DARKGREY+""".--. ||"""+BLUE+"""M"""+DARKGREY+""".--. ||"""+BLUE+"""E"""+DARKGREY+""".--. |.-.  |"""+BLUE+"""P"""+DARKGREY+""".--. ||"""+BLUE+"""L"""+DARKGREY+""".--. ||"""+BLUE+"""A"""+DARKGREY+""".--. ||"""+BLUE+"""N"""+DARKGREY+""".--. |
| :/\: || (\/) || (\/) || (\/) ((1)) | :/\: || :/\: || (\/) || :(): |
| :\/: || :\/: || :\/: || :\/: |'-.-.| (__) || (__) || :\/: || ()() |
| '--'"""+BLUE+"""G"""+DARKGREY+"""|| '--'"""+BLUE+"""A"""+DARKGREY+"""|| '--'"""+BLUE+"""M"""+DARKGREY+"""|| '--'"""+BLUE+"""E"""+DARKGREY+"""| ((1)) '--'"""+BLUE+"""P"""+DARKGREY+"""|| '--'"""+BLUE+"""L"""+DARKGREY+"""|| '--'"""+BLUE+"""A"""+DARKGREY+"""|| '--'"""+BLUE+"""N"""+DARKGREY+"""|
`------'`------'`------'`------'  '-'`------'`------'`------'`------'

"""+BLUE+"""   ______                              _______  __                                                                  
 .' ___  |                            |_   __ \[  |                                                                 
/ .'   \_|  ,--.   _ .--..--.  .---.    | |__) || |  ,--.   _ .--.                                                  
| |   ____ `'_\ : [ `.-. .-. |/ /__\\\   |  ___/ | | `'_\ : [ `.-. |                                                 
\ `.___]  |// | |, | | | | | || \__.,  _| |_    | | // | |, | | | |                                                 
 `._____.' \\'-;__/[___||__||__]'.__.' |_____|  [___]\\'-;__/[___||__]  
 
 
"""+DARKGREY+"""- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"""+NC)


def ParseArguments():


    global directory
    global create
    global target
    global wordlist
    global search
    global outputTags



    parser = argparse.ArgumentParser(description='GamePlan is a tool that searches a collection of commands to find the commands that best suit your pentesting needs.')

    parser.add_argument("-d", "--dir", dest="directory",
                        help="location of directory to save to or to use to create reporing directory")

    parser.add_argument("-t", "--target", dest="target",
                        help="The IP, URL or filename of the target")

    parser.add_argument("-w", "--wordlist", dest="wordlist",
                        help="location of wordlist")

    parser.add_argument("-c", "--create", dest="create",
                        help="name of the file to create")

    parser.add_argument("-s", "--search", dest="search",
                        help="enter the attack(s) tags you want to search for, seperate tags via ,")

    parser.add_argument("-o", "--tags", dest="outputTags", action="store_true",
                        help="Output list of tags")


    args = parser.parse_args()
    
    directory=args.directory
    target=args.target
    create=args.create
    wordlist=args.wordlist
    search=args.search
    outputTags=args.outputTags


def Options():
    
    ########################################
    # change results based on options selected
    ########################################

    global directory
    global create
    global target
    global wordlist
    global search
    global outputTags

    if (outputTags == True):
        #output the tags
        allTags=[]
        with open("searchtags.csv","r") as tagsFile:
            lines = csv.reader(tagsFile)
            for component in lines:
                allTags.append(component)

            print(BLUE+"- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"+NC)
            print(BLUE+""" ___           _ _    _       _____               _ 
| _ \___ _____(_) |__| |___  |_   _|_ _ __ _ ___ (_)
|  _/ _ (_-<_-< | '_ \ / -_)   | |/ _` / _` (_-<  _ 
|_| \___/__/__/_|_.__/_\___|   |_|\__,_\__, /__/ (_)
                                       |___/        """+NC)
            print(BLUE+"- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"+NC)  
            searchList(allTags)
            exit(0)
        
    if create:
        #if not empty
        #create the reporting directory
        if directory:
            #if not empty
            createDir()
            exit(0)
        else:
            print(RED+"Directory tag [-d, --dir] required to create a reporing directory"+NC)
    elif search:
        if target:
            #if not empty
            #search against the entered tags
            
            if not directory:
                directory = "<enter output directory>"
            if not wordlist:
                wordlist = "<enter wordlist directory>"
                
            searchTags()
            exit(0)

        else:
            print(RED+"Target tag [-t, --target] required"+NC)
        

def YesNo(question):
    ########################################
    # Call to pose a yes no option
    ########################################
    #arg 1 = Question to ask

    accept = False
        
    #loop untill a acceptable option is selected
    #echo to >&2 (error) so value isnt returned
    while (accept == False):

        print(DARKGREY+"- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"+NC)
        print(BLUE+question+NC)
        print(RED+"[0]"+NC+" - no")
        print(GREEN+"[1]"+NC+" - yes")
        print(DARKGREY+"- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"+NC)
        responce = input()    

        if (responce == "0"): 
            accept=True
            answer=False
        elif (responce == "1"):
            accept=True	
            answer=True
        else:
            print(RED+"Incorrect Input"+NC)


    return answer
	

def createDir():

    ########################################
    # Create Reporting Directory
    ########################################

    #Ask what folders to create
    webFolder=YesNo("Create web folder?")
    hashFolder=YesNo("Create hashes folder?")
    exploitFolder=YesNo("Create exploit folder?")
    imageFolder=YesNo("Create image folder?")
    bruteFolder=YesNo("Create bruteforce folder?")

    #Ask the directory names to an array for later
    folders=["report","nmap_scans"]
	
    if ( webFolder == True ):
        folders.append("web")

    if ( hashFolder == True ):
        folders.append("hashes")

    if ( exploitFolder == True ):
        folders.append("exploits")

    if ( imageFolder == True ):
        folders.append("images")

    if ( bruteFolder == True ):
        folders.append("bruteforce")

    
    #create a string copy to show to user for them to accept
    foldersMsg="Create reporting directory: "+create+NC+"\nIn location "+DARKGREY+directory+"/"+BLUE+create+NC+"\nWith the following folders:"+BLUE+"\n"+str(folders)

    #make sure user is happy with location and folders before creating
    accepted=YesNo(foldersMsg)

    #If they accept create the actuakl folders
    if (accepted == True):
        print(DARKGREY+"- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"+NC)
        print(BLUE+"Creating reporting directory"+NC)
        for dir in folders:
        
            command="mkdir -p "+directory+"/"+create+"/"+dir
            os.system(command)
            print("Created directory :"+DARKGREY+directory+"/"+create+"/"+BLUE+dir+NC)
        
        
        #create the reporting text file
        now = datetime.datetime.now()
        command="echo \"- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -\nPentest of : "+target+"\nDate : "+now.strftime("%h %d %Y")+"\nTime : "+now.strftime("%H:%M:%S")+"\n- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -\" >> "+directory+"/"+create+"/report/report.txt"
        os.system(command)

    else:
        exit(0)


def formatting(commands):

    ########################################
    # Format the commands in the same way
    ########################################
    #0 = tags
    #1 = Title
    #2 = commands
    #3 = description
    #4 = matches

    #sort the order by the number of matches
    commands=sorted(commands, key=lambda x: x[4], reverse=False) # don't reverse so most matches are at end / seen first

    #create an id based on current time
    now = datetime.datetime.now()
    ID=now.strftime("%h_%d_%H%M%S")

    if "http" in target:
        url = target
        print(url)
    else:
        url = "http://URL"
    

    for command in commands:

        #replace placeholders with live values
        command[2] = command[2].replace("$target", target)
        command[2] = command[2].replace("$wordlist", wordlist)
        command[2] = command[2].replace("$directory", directory)
        command[2] = command[2].replace("$ID", ID)
        command[2] = command[2].replace("$URL", url)
        
        #seperate tags into a string
        tags=""
        for tag in command[0]:
            tags+=" | "+tag

        #add colours and newlines to description
        command[3] = command[3].replace("\\n", "\n")
        command[3] = command[3].replace("$RED", RED)
        command[3] = command[3].replace("$DARKGREY", DARKGREY)
        command[3] = command[3].replace("$BLUE", BLUE)
        command[3] = command[3].replace("$NC", NC)

        time.sleep(0.8)
        print(DARKGREY+"- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -\n"+NC)
        print(DARKGREY+command[1]+NC)
        print(BOLD+"Tags:"+tags+NC)
        print(command[3])
        print(BLUE+"\n"+command[2]+NC+"\n")
        print(DARKGREY+"- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"+NC)

    
def searchList(tags):

    ########################################
    # Display the definitions of the tags
    ########################################
    #0 = Tag
    #1 = Title
    #2 = description

    for tag in tags:

        time.sleep(0.4)
        print(BLUE+"- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"+NC)
        print(BLUE+tag[1]+NC)
        print(BOLD+"Tag : <"+tag[0]+">"+NC)
        print(tag[2])
        print(BLUE+"- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"+NC)


def searchTags():

    ########################################
    # filter through results
    ########################################

    results=[]
    
    tags=search.replace(" ", "").split(",") #clean spaces and seperate tags via ,
    
    #read through the commands csv 
    with open("commands.csv","r") as commandsFile:
        lines = csv.reader(commandsFile)
        for component in lines:
            component[0] = component[0].split(',') #split the tags into an array

            count=0 # The number of tags that match
            #loop through the searched tags
            for tag in tags:
                if tag in component[0]:
                    #if the tag being searched is included in the command add it to the count
                    count+=1
            if (count > 0):
                #if at least one match with the tags add to list
                component.append(count)
                results.append(component)
            
    tagResults=[]

    with open("searchtags.csv","r") as tagsFile:
        lines = csv.reader(tagsFile)
        for component in lines:
            
            for tag in tags:
                if tag in component[0].lower():
                    #if the tag being searched is included in the command add it to the list
                    tagResults.append(component)
            

    print(BLUE+"- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"+NC)
    print(BLUE+""" ___                  _           _   _____               _ 
/ __| ___ __ _ _ _ __| |_  ___ __| | |_   _|_ _ __ _ ___ (_)
\__ \/ -_) _` | '_/ _| ' \/ -_) _` |   | |/ _` / _` (_-<  _ 
|___/\___\__,_|_| \__|_||_\___\__,_|   |_|\__,_\__, /__/ (_)
                                               |___/        """+NC)
    print(BLUE+"- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"+NC)        
    searchList(tagResults)
    
    print(DARKGREY+"- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"+NC)
    print(DARKGREY+"""  ___                              _      ___                 _   _ 
 / __|___ _ __  _ __  __ _ _ _  __| |___ | __|__ _  _ _ _  __| | (_)
| (__/ _ \ '  \| '  \/ _` | ' \/ _` (_-< | _/ _ \ || | ' \/ _` |  _ 
 \___\___/_|_|_|_|_|_\__,_|_||_\__,_/__/ |_|\___/\_,_|_||_\__,_| (_)"""+NC)

    print(DARKGREY+"- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"+NC)   
    formatting(results)


ParseArguments()
Banner()
Options()