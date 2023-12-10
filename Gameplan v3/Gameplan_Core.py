#!/usr/bin/env python3

###########################################
# Project : GamePlan 
# File : Gameplan_Core.py
# Version : 3.0.1

###########################################
# Author : Connor Maddison
# Creation Date : 10/12/2023
###########################################



import yaml
import re
from os.path import isfile, dirname
from os import listdir
import logging


    

class Gameplan_Core:

    #-------------------------------------------------------------------------------------------------------------
    # Logging
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%d-%b-%Y %H:%M',
                        filename=f'{dirname(__file__)}/Gameplan.log',
                        filemode='a')

    CONSOLELOG = logging.StreamHandler()
    CONSOLELOG.setLevel(logging.WARNING)
    CONSOLELOG.setFormatter(logging.Formatter('%(levelname)-8s: %(message)s'))
    logging.getLogger('').addHandler(CONSOLELOG)
    #-------------------------------------------------------------------------------------------------------------


    def __init__(self):
        #Send in core values, e.g. IP / TARGET????
        self.target = '10.10.10.10'
        ##TEMP
        self.IP = '10.10.10.10'
        self.WORDLIST = 'THIS'
        #-------------------------------------------------------------------------------------------------------------
        # GLOBALS
        self.CURRENT_PATH = dirname(__file__)
        self.COMMAND_LIST = []
        self.TAGS_LIST = {}
        self.AUTHORS_LIST = {}
        self.PACKAGES_LIST = {}
        self.FILTERS = {}

        self.Import_All_Commands()        
        self.FILTERS = self.Create_Empty_Command_File(self.COMMAND_LIST[0])
        
        
        #-------------------------------------------------------------------------------------------------------------
        
    def Format_Command(self, unformatted_command):

        format_command = unformatted_command
        ##Extract all the tags in the standard format
        extract_tags = re.findall("{{\w*}}", format_command)

        if extract_tags is None:
            logging.info('No command tags found')
            return format_command

        for tag in extract_tags:
            tag_element = re.split("}}", re.split("{{", tag)[1])[0]
            
            match tag_element:
                ## Match the extracted tag to the correct official tags
                case 'IP':
                        format_command = re.sub("{{IP}}",self.IP,format_command)
                case 'WORDLIST':
                        format_command = re.sub("{{WORDLIST}}",self.WORDLIST,format_command)
                case n:
                      logging.warning(f'Invalid command tag found : {tag_element}')

        logging.info('Command formatted')
        return format_command
    

    def CSV_To_List(self, csv):
        split_file = re.split(",",csv)
        lower = []
        for value in split_file:
            value = value.lower().lstrip()
            lower.append(value)

        split_file = lower 
        return lower


    def Read_Yaml_File(self, filename):
        ext = re.split("\.",filename)[-1]
        if ext not in ['yaml', 'yml']:
            logging.error(f'Incorrect extension : {filename}')
            return None
        logging.debug(f'Correct extension : {ext}')

        if isfile(f'{self.CURRENT_PATH}/commands/{filename}') is False:
            logging.error(f'File doesn\'t exist: {self.CURRENT_PATH}/commands/{filename}')
            return None
        logging.debug(f'File found {filename}')

        with open(f'{self.CURRENT_PATH}/commands/{filename}', 'r') as yaml_file:
            command_file = yaml.safe_load(yaml_file)
        logging.info('Yaml file converted')

        ## Convert csv format to dict
        command_file['info']['tags'] = self.CSV_To_List(command_file['info']['tags'])
        command_file['info']['required_packages'] = self.CSV_To_List(command_file['info']['required_packages'])
        command_file['info']['author(s)'] = self.CSV_To_List(command_file['info']['author(s)'])


        return command_file
    

    def Import_All_Commands(self):
        command_dir = listdir(f'{self.CURRENT_PATH}/commands')
        for command_file in command_dir:
            returned_yaml = self.Read_Yaml_File(command_file)
            if returned_yaml is not None:
                self.COMMAND_LIST.append(returned_yaml)
        logging.info('Loaded commands')
        self.Gather_Info()


    def Create_Empty_Command_File(self, command_dict):

        ## Basically creates an empty copy of the command yml file format by clearing out an existing one
        level_dict = {}
        for key, value in command_dict.items():
            if type(value) == dict:
                nested_dict = self.Create_Empty_Command_File(value)
                level_dict.update({key: nested_dict})
            else:
                level_dict.update({key: []})
        return level_dict

    def Gather_Info(self):
        #go through all commands info and gather usefull facts and tags that can be filtered on

        for command in self.COMMAND_LIST:
            try: 
                ## TAGS
                for tag in command['info']['tags']:
                    tag = tag.lower().lstrip()
                    if tag not in self.TAGS_LIST:
                        self.TAGS_LIST.update({tag:1})
                    else:
                        self.TAGS_LIST.update({tag:self.TAGS_LIST[tag]+1})
            except:
                logging.error(f'Failed to find tags for: {command["info"]["summary"]}')

            try:
                ## PACKAGES
                for package in command['info']['required_packages']:
                    package = package.lower().lstrip()
                    if package not in self.PACKAGES_LIST:
                        self.PACKAGES_LIST.update({package:1})
                    else:
                        self.PACKAGES_LIST.update({package:self.PACKAGES_LIST[package]+1})
            except:
                logging.error(f'Failed to find packages for: {command["info"]["summary"]}')
            
            try:
                for author in command['info']['author(s)']:
                    author = author.lower().lstrip()
                    if author not in self.AUTHORS_LIST:
                        self.AUTHORS_LIST.update({author:1})
                    else:
                        self.AUTHORS_LIST.update({author:self.AUTHORS_LIST[author]+1})
            except:
                logging.error(f'Failed to find author(s) for: {command["info"]["summary"]}')

            logging.info(f'Loaded info for {command["info"]["summary"]}')
                 

#test = Gameplan_Core()


#works = Gameplan_Core.Read_Yaml_File('demo.yml')
#print(Gameplan_Core.Format_Command(works['command']))   
