#!/usr/bin/env python3

###########################################
# Project : GamePlan 
# File : Gameplan_GUI.py
# Version : 0.0.1

###########################################
# Author : Connor Maddison
# Creation Date : 10/12/2023
###########################################

import PySimpleGUI as sg
from Gameplan_Core import Gameplan_Core
import customtkinter as ctk

ctk.set_appearance_mode("System")

ctk.set_default_color_theme("dark-blue")  
###########################################
# COLOURS
# CORE:
GREY100= "#161616"
GREY60 = "#1a1a1a"
GREY30 = "#242424"
GREY10 = "#2e2e2e"

DARK_ACCENT = "#2b1a47"
LIGHT_ACCENT = "#553784"
DARK_SECOND = "#110c1f"
LIGHT_SECOND = "#1f2887"

DARK_SUCCESS = "#225423"
LIGHT_SUCCESS = "#4caf50"


#
#
#
###########################################

class Tags_Frame(ctk.CTkFrame):
    def __init__(self, master, tags):
        super().__init__(master)
        self.tags = tags
        self.configure(fg_color="transparent")

        self.grid(row=0, column=1, padx=(15,5), pady=5, sticky="ew", rowspan="2")
        self.anchor = "e"

        #self.tags_label = ctk.CTkLabel(self, text="Filter Tags", fg_color="transparent",justify="left", anchor="w",font=('Arial',12, "bold"))
        #self.tags_label.grid(row=0, column=0, padx=5, pady=(5,10), sticky="ew", columnspan="5")

        ## | | | |  x5 columns

        row_step = 1
        col_step = 0
        for tag_split in tags:
            for tag in tag_split:
                print(tag)
                self.tag = ctk.CTkButton(self,
                                        text=tag, 
                                        anchor="center", 
                                        font=('Arial',12),
                                        width=80,
                                        fg_color=LIGHT_SECOND,
                                        hover_color=DARK_SECOND)
                self.tag.grid(row=row_step, column=col_step, padx=5, pady=5, sticky="ew")
                if col_step >= 4:
                    col_step = 0
                    row_step += 1
                else:
                    col_step += 1





class Command_Frame(ctk.CTkFrame):
    def __init__(self, master, set_row, info):
        super().__init__(master)
        self.info = info
        self.configure(fg_color=GREY30, corner_radius=15)

        self.grid(row=set_row, column=0, padx=5, pady=5,sticky="ew")
        self.grid_columnconfigure(0, weight=9)
        self.grid_columnconfigure(1, weight=1)

        ## Summary of vuln
        summary_text = info["info"]["summary"]
        if len(summary_text) >= 70:
            summary_text = f'{summary_text[:67]}...'
        self.summary = ctk.CTkLabel(self, text=str(summary_text), fg_color="transparent",justify="left", anchor="w", font=('Arial',24,"bold"), wraplength=600)
        self.summary.grid(row=0, column=0, padx=(15,200), pady=(15,3), sticky="ew")
        
        self.creation_container = ctk.CTkFrame(self, fg_color="transparent")
        self.creation_container.grid(row=1, column=0, padx=(30,5), pady=(5,10),sticky="new")
        self.creation_container.anchor= "nw"
        ## date created | last updated
        date_note = f'Created: {info["info"]["date_created"]}  |  Last Updated: {info["info"]["last_updated"]}'
        self.date_created = ctk.CTkLabel(self.creation_container, text=str(date_note), fg_color="transparent",justify="left", anchor="w",font=('Arial',12, "bold"))
        self.date_created.grid(row=0, column=0, padx=0, pady=0, sticky="ew")
        ## author
        authors_stack = ""
        for author in info["info"]["author(s)"]:
            authors_stack += f'{author}'
            if author != info["info"]["author(s)"][-1]:
                authors_stack += ', '
            
        self.author = ctk.CTkLabel(self.creation_container, text=str(authors_stack), fg_color="transparent",justify="left", anchor="w", font=('Arial',12))
        self.author.grid(row=1, column=0, padx=0, pady=0, sticky="ew")

        ## action buttons
        self.action_container = ctk.CTkFrame(self, fg_color="transparent")
        self.action_container.grid(row=2, column=0, padx=30, pady=(10,20),sticky="sew")
        self.action_container.anchor= "sw"

        self.expand = ctk.CTkButton(self.action_container,
                                    text="expand", 
                                    anchor="center", 
                                    font=('Arial',12),
                                    width=240,
                                    fg_color=LIGHT_ACCENT,
                                    hover_color=DARK_ACCENT)
        self.expand.grid(row=0, column=0, padx=(0,15), pady=0, sticky="ne")

        self.run = ctk.CTkButton(self.action_container,
                                    text="run", 
                                    anchor="center", 
                                    font=('Arial',12),
                                    width=100,
                                    fg_color=LIGHT_SUCCESS,
                                    hover_color=DARK_SUCCESS)
        self.run.grid(row=0, column=1, padx=(15,0), pady=0, sticky="ne")


        ## -> Tags,packages (as buttons?)

        self.tags = Tags_Frame(self, [info["info"]["tags"],info["info"]["required_packages"]])


       
        



class Filters_Segment_Frame(ctk.CTkFrame):
    def __init__(self, master, set_row, set_values, set_type):
        super().__init__(master)
        self.values = set_values
        self.type = set_type
        self.active = []
        self.segments = {}

        self.configure(fg_color="transparent")
        self.grid(row=set_row, column=0, padx=5, pady=5,sticky="ew")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        for index, (key, value) in enumerate(self.values.items()):

            self.switch_var = ctk.StringVar(value="off")
            self.switch = ctk.CTkSwitch(self, 
                                   text=key, 
                                   onvalue="on", 
                                   offvalue="off",
                                   variable=self.switch_var,
                                   command = lambda filter_type=set_type, filter=key: self.Trigger_filter(filter_type,filter),
                                   progress_color=LIGHT_ACCENT)
            self.switch.grid(row=index, column=0, padx=10, pady=5, sticky="ew")
            
            self.current = ctk.CTkLabel(self, text=value, fg_color="transparent",justify="right",anchor="e")
            self.current.grid(row=index, column=1, padx=10, pady=5, sticky="ew")
            self.segments.update({key:[self.switch, self.current]})


    def Parse_Filters(self, filter_dict, filter_type, filter, modifier=True):

        ## Modifier True = Add, False = Del
        if filter_dict is None or filter_type is None or filter is None:
            return None

        for key, value in filter_dict.items():
            if key != filter_type and type(value) == dict:
                self.Parse_Filters(value, filter_type, filter, modifier)
            elif key == filter_type:
                
                if modifier:
                    if filter not in value:
                        value.append(filter)
                else:
                    if filter in value:
                        value.remove(filter)


        
    def Trigger_filter(self, filter_type=None, filter=None):

        if filter_type is None or filter is None:
            return

        global GAMEPLAN_SESSION

        if filter not in self.active:
            self.active.append(filter)
            self.Parse_Filters(GAMEPLAN_SESSION.FILTERS, filter_type, filter, True)
            
        else:
            self.active.remove(filter)
            self.Parse_Filters(GAMEPLAN_SESSION.FILTERS, filter_type, filter, False)

        


class Filters_Frame(ctk.CTkFrame):
    def __init__(self, master, set_row, set_column, set_values):
        super().__init__(master)
        self.values = set_values
        self.segments = {}
        self.width = 20
        self.anchor("w")
        self.grid(row=set_row, column=set_column, padx=0, pady=0,sticky="nsew")
        self.configure(fg_color=GREY100)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure([0,1],weight=1)
        self.grid_rowconfigure(2,weight=19)      
                


        self.main_header = ctk.CTkLabel(self, text="Filters:", fg_color="transparent",justify="left", anchor="w",font=('Arial',24,"bold"))
        self.main_header.grid(row=0, column=0, padx=20, pady=(20,0), sticky="ew", columnspan="3")  
        self.search = ctk.StringVar()
        self.search.trace("w", lambda name, index, mode, trigger=self.search: self.filter_by_text(trigger))
        self.search_bar = ctk.CTkEntry(self, placeholder_text="Filter", textvariable=self.search, fg_color=GREY10)
        self.search_bar.grid(row=1,column=0, padx=20, pady=(5,20), sticky="ew", columnspan="3")

        self.filters_container = ctk.CTkScrollableFrame(self, fg_color=GREY60)
        self.filters_container.grid(row=2, column=0, padx=20, pady=0,sticky="nsew")
        self.filters_container.grid_columnconfigure(0, weight=19)
        self.filters_container.grid_columnconfigure([1,2], weight=1)

        rows = 0
        for index, (key, value) in enumerate(self.values.items()):
            
            self.header = ctk.CTkLabel(self.filters_container, text=key, fg_color="transparent",justify="left", anchor="w",font=('Arial',16,"bold"))
            self.header.grid(row=rows, column=0, padx=10, pady=5, sticky="ew")
            self.header.bind("<Button-1>", lambda e,i=index: self.toggle(i))
            self.totals = ctk.CTkLabel(self.filters_container, text=len(value), fg_color="transparent",justify="right", anchor="e")
            self.totals.grid(row=rows, column=1, padx=10, pady=5, sticky="ew", )
            self.totals.bind("<Button-1>", lambda e,i=index: self.toggle(i))

            self.toggle_btn = ctk.CTkButton(self.filters_container,
                                            text="-",
                                            command=lambda i=index: self.toggle(i),
                                            width=30,
                                            height=30,
                                            fg_color="transparent", 
                                            text_color=("gray10", "gray90"),
                                            hover_color=("gray70", "gray30"), 
                                            anchor="center")
            self.toggle_btn.grid(row=rows, column=3, padx=10, pady=5, sticky="nsew")
            rows += 1
            self.filters_segment_frame = Filters_Segment_Frame(self.filters_container,rows,value,key)
            self.segments.update({index:[self.filters_segment_frame,self.totals,self.toggle_btn]})
            rows += 1
            


    def toggle(self, index=None):
        if index is None:
            return
        if self.segments[index][0].winfo_viewable():
            self.segments[index][0].grid_remove()
            self.segments[index][2].configure(text="+")
        else:
            self.segments[index][0].grid()
            self.segments[index][2].configure(text="-")
    
        
    def filter_by_text(self, trigger):
        input = self.search_bar.get()

        for index, segment in self.segments.items():      ## index : [segment, total]
            ammount = 0

            for name, reference in segment[0].segments.items():
                
                if input not in name:
                    reference[0].grid_remove()
                    reference[1].grid_remove()
                else:
                    ammount += 1
                    reference[0].grid()
                    reference[1].grid()

            
            if ammount <= 0:
                if segment[0].winfo_viewable():
                    segment[0].grid_remove()
            else:
                if not segment[0].winfo_viewable():
                    segment[0].grid()
            segment[1].configure(text=ammount)

        

        


class App(ctk.CTk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Gameplan v2.0")

        global GAMEPLAN_SESSION
        GAMEPLAN_SESSION = Gameplan_Core()
        KNOWN_FILTERS = {}
        KNOWN_FILTERS.update({'tags' : GAMEPLAN_SESSION.TAGS_LIST})
        KNOWN_FILTERS.update({'required_packages' : GAMEPLAN_SESSION.PACKAGES_LIST})
        KNOWN_FILTERS.update({'author(s)' : GAMEPLAN_SESSION.AUTHORS_LIST})

        self.geometry("1100x650")
        self.resizable(width=True,height=True)
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=8)
        self.grid_rowconfigure(0, weight=1)

        self.filters_frame = Filters_Frame(self,0,0,KNOWN_FILTERS)

        self.command_container = ctk.CTkScrollableFrame(self, fg_color=GREY60)
        self.command_container.anchor = "w"
        self.command_container.grid(row=0, column=1, sticky="nsew")
        for index, command in enumerate(GAMEPLAN_SESSION.COMMAND_LIST):
            self.command = Command_Frame(self.command_container,index,command)

        #self.textbox = ctk.CTkTextbox(master=self, width=400, corner_radius=15)
        #self.textbox.grid(row=0, column=1, sticky="nsew")
        #self.textbox.insert("0.0", "Some example text!\n" * 50)

        

app = App()
app.mainloop()



quit()

sg.theme('DarkTeal10')

# First the window layout in 2 columns

search_bar = [
    sg.Text("Filter"),
    sg.In(enable_events=True, 
          key="-FILTER-",
          expand_x=True
          ) 
]


tags_headings = ['Tag', 'Count']
packages_headings = ['Packages', 'Count']
authors_headings = ['Authors', 'Count']
rc_filter_commands = ['&filter', ['TEST::TEST','Filter on', 'Add to current filter']]

filters_column = [

    [sg.Table(values=[], 
        headings=tags_headings,
        auto_size_columns=True,
        justification='left',
        key='-KNOWN TAGS-',
        expand_x=True,
        expand_y=True,
        enable_events=True,
        select_mode=sg.TABLE_SELECT_MODE_BROWSE)],
    [sg.Table(values=[], 
        headings=packages_headings,
        auto_size_columns=True,
        justification='left',
        key='-KNOWN PACKAGES-',
        expand_x=True,
        expand_y=True,
        enable_click_events=True,
        enable_events=True,
        select_mode=sg.TABLE_SELECT_MODE_BROWSE)],
    [sg.Table(values=[], 
        headings=authors_headings,
        auto_size_columns=True,
        justification='left',
        key='-KNOWN AUTHORS-',
        expand_x=True,
        expand_y=True,
        enable_click_events=True,
        enable_events=True,
        select_mode=sg.TABLE_SELECT_MODE_BROWSE)],   
    

]

output_block = [

    sg.Column(filters_column, expand_y=True, expand_x=True, right_click_menu=rc_filter_commands),
    #filters_column,
    sg.VSeperator(),

    sg.Listbox(
            values=[], 
            enable_events=True, 
            key="-FILTER RETURNS-",
            expand_x=True,
            expand_y=True
        )
]


# ----- Full layout -----
layout = [
    [
        search_bar
    ],
    [
        output_block
    ]
]

window = sg.Window("Gameplan v2.0", layout, size=(700,450), resizable=True)
GAMEPLAN_SESSION = Gameplan_Core()

# Run the Event Loop
while True:
    event, values = window.read()

    known_tags = list(GAMEPLAN_SESSION.TAGS_LIST.items())
    

    window["-KNOWN TAGS-"].update(known_tags)
    window["-KNOWN PACKAGES-"].update(list(GAMEPLAN_SESSION.PACKAGES_LIST.items()))
    window["-KNOWN AUTHORS-"].update(list(GAMEPLAN_SESSION.AUTHORS_LIST.items()))

    if event == "Exit" or event == sg.WIN_CLOSED:
        break

    print(event, values)

    if event == '-KNOWN TAGS-':
        try:
            selected_tag = known_tags[values[event][0]][0]
            print(selected_tag)
        except:
            pass
        
        #print(known_tags[int(values[event])][0])
        

    if event == "-FILTER-":
        filter_request = values["-FILTER-"]
        #try:
            
        #except:

        filter_list = [filter_request] # temp

        window["-FILTER RETURNS-"].update(filter_list)
    

window.close()