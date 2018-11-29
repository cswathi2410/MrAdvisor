# -*- coding: utf-8 -*-
"""
Created on Thu Nov 15 12:27:10 2018

@author: Kevin
"""

import csv
import calendar_tools
from advisor import advisor, restructure

class Calendar:
    """
    Create a calendar which contains the events
    """
    
    def __init__(self):
        """
        Initialize a calendar as a list
        """
        self.cal = []

#    def load_old(self,file):
#        """
#        Load events in the calendar from an external file
#        """
#        with open(file) as fp:
#            reader = csv.DictReader(fp)
#            self.cal = list(reader)
    
    def load(self,file_path: str)->list:
        """
        reads the csv table named file_name and converts it to a list of dicts. 
        Note that in the path, '\' has to be replaced with '/'
        """
        file = open(file_path,'r')
        temp_cal = []
        for row in csv.DictReader(file):
            temp_entry = {}
            temp_entry['id']= len(temp_cal)
            for k, v in row.items():
                temp_entry[k] = v
            temp_entry['clash'] = []
            temp_entry['attend'] = 1
            temp_entry['tie'] = 0
            temp_cal.append(temp_entry)
        self.cal = calendar_tools.clean(temp_cal)
        
    def fill(self, month_number: int):
        """
        Fill an empty month with the events in the calendar and return a csv file of the month
        """
        #Extract the events for the relevant month
        sub_cal = [] #list(month) of dict(event)
        for i in self.cal:
            if i['month'] == month_number:
                sub_cal.append(i)
        
        #Template for the month
        month_cal = calendar_tools.create_empty_calendar(month_number) #list(month) of dict(event)
        
        #Filling the template according to the advisor
        if sub_cal:
            new_sub = advisor(sub_cal,month_number) #warning: change in structure: list(month) of list(days) of dict(event)
            for i in new_sub:
                print('sub_cal is: '+str(new_sub))
                print('i in sub_cal: '+str(i)+" "+str(len(i)))
                for j in range(len(i)):
                    print('j in i: '+str(j))
                    if i[j]['attend']:
                        start_pos = calendar_tools.hourToPosition(i[j]['start'])
                        end_pos = calendar_tools.hourToPosition(i[j]['end'])-1
                        date = calendar_tools.dayFormat(i[j]['day'],i[j]['month'])
                        for k in range(start_pos,end_pos+1):
                            month_cal[k][date] = i[j]['title']
                    else: 
                        None
        #Writing in the file
        file_name = f"{calendar_tools.DICT_MONTHS[month_number]['month']}.csv"
        calendar_tools.write(file_name,month_cal)
        print(f"Calendar ready in {file_name}")


            
    
          