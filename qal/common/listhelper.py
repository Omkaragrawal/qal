'''
Created on Oct 10, 2010

@author: Nicklas Boerjesson
@note: Helper functions for list types
'''

def CI_index(_List, _value):
    """Finds an item in a list"""
    if _value != None:
        for index in range(len(_List)):
            if _List[index].lower() == _value.lower():
                return index
    
    return -1;

def unenumerate(value, _Type):
    """Returns the value of a specific type""" 
    return value[_Type]   

def find_next_match(self, _list, _start_idx, _match):
    for _curr_idx in range(_start_idx, len(_list)):
        if _list[_curr_idx] == _match:
            return _curr_idx
    return -1

def find_previous_match(self, _list, _start_idx, _match):
    for _curr_idx in range(_start_idx, 0, -1):
        if _list[_curr_idx] == _match:
            return _curr_idx
    return -1
