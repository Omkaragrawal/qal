'''
Created on Sep 14, 2012

@author: Nicklas Boerjesson
'''


from qal.nosql.custom import Custom_Dataset

import csv
import os

class Flatfile_Dataset(Custom_Dataset):
 
    """This class loads a flat file into an array."""
    delimiter = None
    filename = None
    has_header = None
    csv_dialect = None
    field_names = None
    
    def __init__(self, _delimiter = None, _filename = None, _has_header = None, _csv_dialect = None, _resource = None):
        """Constructor"""
        
        if _resource != None:
            self.read_resource_settings(_resource)
        else:
            if _delimiter != None: 
                self.delimiter = _delimiter
            else:  
                self.delimiter = None    
            if _filename != None: 
                self.filename = _filename
            else:
                self.filename = None      
            if _has_header != None: 
                self.has_header = _has_header
            else:
                self.has_header = None
                  
            if _csv_dialect != None: 
                self.csv_dialect = _csv_dialect
            else:
                self.csv_dialect = None      
             
        super(Flatfile_Dataset, self ).__init__()
        
    def read_resource_settings(self, _resource):
        if _resource.type.upper() != 'FLATFILE':
            raise Exception("Flatfile_Dataset.read_resource_settings.parse_resource error: Wrong resource type")
        self.filename =    _resource.data.get("filename")
        self.delimiter =   _resource.data.get("delimiter")
        self.has_header =  bool(_resource.data.get("has_header"))
        self.csv_dialect = _resource.data.get("csv_dialect")

    def load(self):
        """Load data"""
        _tmp_dir_abs = os.getcwd() 
        print("Flatfile_Dataset.load: Filename='"+str(os.path.normpath(_tmp_dir_abs +'/' + self.filename)) + "', Delimiter='"+str(self.delimiter)+"'")
        
        _file = open(os.path.normpath(_tmp_dir_abs +'/' + self.filename), 'r')
        _reader = csv.reader(_file, delimiter=self.delimiter, quoting=csv.QUOTE_NONE)
        _first_row = True
        self.data_table = []
        for _row in _reader:
            # Save header row if existing.
            if (_first_row and self.has_header == True):
                self.field_names = [_curr_col.replace("'", "") for _curr_col in _row]
                print("self.field_names :" + str(self.field_names))
                _first_row = False
            else:
                self.data_table.append(_row)
                    
            
            
        if (self.has_header == False):
            for _curr_idx in range(0,len(_reader[0])):
                self.field_names.append("Field_"+ str(_curr_idx))   
            
        return self.data_table        