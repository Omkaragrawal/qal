"""
Created on Sep 13, 2013

@author: Nicklas Börjesson
@note: This module contains access functionality for resources.
"""
from qal.common.xml_utils import XML_Translation

from lxml import etree


def add_xml_subitem(_parent, _nodename, _nodetext):
    _curr_item = etree.SubElement(_parent, _nodename)
    _curr_item.text = str(_nodetext)
    return _curr_item


def resource_types():
    """Returns a list of the supported resource types"""
    return ["CUSTOM", "FLATFILE", "MATRIX", "XPATH", "RDBMS"]

class Resource(object):
    
    uuid = None
    type = None
    caption = None
    
    data = {}
    
    def __init__(self):
        self.uuid = None
        self.type = None
        self.caption = None    
        self.data = {}
        
    def as_xml(self):
        """This function encode an XML structure into resource objects. Uses lxml as opposed to parse_xml()."""
        _resource = etree.Element("resource")
        _resource = etree.SubElement("uuid")
        
        add_xml_subitem(_resource, "uuid", self.uuid) 
        
        
        return _resource
    

class Resources(XML_Translation):
    '''
    The resource class provides access to resources available through either XML-definitions or callback functions.
    '''
    
    """Local list of resources"""
    local_resources = None
    """Callback method for external lookup"""
    external_resources_callback = None


    def __init__(self, _resources_node=None, _resources_xml=None, _external_resources_callback=None):
        '''
        The argument _resources_node is an XML node from which local resources are parsed. 
        The argument _external_resources_callback is a user provided callback function 
        that has the same arguments as the get_resource-function.  
        '''
       
        if _resources_node != None or _resources_xml != None:
            self.parse_xml(_resources_node, _resources_xml)
                    
    def get_resource(self, _uuid):
        
        _resource = None
        
        """Check local list"""
        if self.local_resources and _uuid in self.local_resources:
            _resource = self.local_resources[_uuid]
        
        """Lookup externally"""
        if (_resource == None) and (self.external_resources_callback):
            _resource = self.external_resources_callback(_uuid)
        
        if _resource == None:
            raise Exception("get_resource: Resource not found - uuid: " + _uuid)
        else:
            return _resource
     
    
    
    def parse_xml(self, _resources_node=None, _resources_xml=None):
        """This function parses an XML structure into resource objects. Should use lxml."""


        if _resources_node == None:
            _parser = etree.XMLParser(remove_blank_text=True)
            _resources_node = etree.fromstring(_resources_xml, _parser)            
            
        
        
        self.local_resources = dict()
        
        for _curr_resource_node in _resources_node.findall("resource"):
            
            if _curr_resource_node.get("uuid") != None:
                self._debug_print("parse_xml: Create new resource object")
                _new_resource = Resource()
                _new_resource.uuid = _curr_resource_node.get("uuid")
                _new_resource.type = _curr_resource_node.get("type")
                _new_resource.caption = _curr_resource_node.get("caption")
                
                for _curr_resource_data in _curr_resource_node.findall("*"):
                    _new_data = []
                    if len(_curr_resource_data.findall("item")) > 0:
                        for _curr_item in _curr_resource_data.findall("item"):
                            _new_data.append(_curr_item.text)
                        _new_resource.data[str(_curr_resource_data.tag).lower()] = _new_data
                        self._debug_print("parse_xml: Add datas "+ str(_curr_resource_data.tag).lower() + " " +  str(_new_resource.data[str(_curr_resource_data.tag).lower()]) , 1)
                                    
                    else:
                        _new_resource.data[str(_curr_resource_data.tag).lower()] = _curr_resource_data.text
                        self._debug_print("parse_xml: Add data "+ str(_curr_resource_data.tag).lower() + " " + _new_resource.data[str(_curr_resource_data.tag).lower()] , 1)
                        
            
                self.local_resources[_new_resource.uuid] = _new_resource
                self._debug_print("parse_xml: Append resource: "+_new_resource.caption + " uuid: " + _new_resource.uuid + " type: " + _new_resource.type  , 4)
    def as_xml(self):
        """This function encode an XML structure into resource objects. Uses lxml as opposed to parse_xml()."""
        #_resources = 
        
        
        
        
        
        return _node