"""
    Tests for resources
    
    :copyright: Copyright 2010-2014 by Nicklas Boerjesson
    :license: BSD, see LICENSE for details.
"""
import json

import unittest
import os
from distlib.util import get_resources_dests
from jsonschema.validators import Draft4Validator
from qal.common.diff import DictDiffer

from qal.common.resources import Resources, Resource, generate_schema

Test_Script_Dir = os.path.dirname(__file__)
Test_Resource_Dir = os.path.join(Test_Script_Dir, 'resources')


class Test(unittest.TestCase):


    def test_1_JSON_parsing(self):

        f = open(Test_Resource_Dir + "/_test_resource_in.json", "r")
        _dict_in = json.loads(f.read())
        f.close()
        _resources = Resources(_resources_list=_dict_in)
        # _resources.debuglevel = 4



        _dict_out = _resources.as_json_dict()

        f_out = open(Test_Resource_Dir + "/_test_resource_out.json", "w")
        print(json.dumps(_dict_out), file=f_out)
        f_out.close()


        self.assertEqual(len(_resources._local_resources), 5, 'Resources are not as many as they should')

        _test_resource = _resources["{1D62083E-88F7-4442-920D-0B6CC59BA2FF}"]
        self.assertIsNotNone(_test_resource, 'Resource data not found')
        self.assertEqual(_test_resource.name, "localhost_pg", 'Resource name do not match')
        f.close()


        _changes = DictDiffer.compare_documents( {"_":_dict_in}, {"_": _dict_out})
        if len(_changes) == 0:
            self.assertTrue(True)
        else:
            DictDiffer.pretty_print_diff(_changes)
            self.assertTrue(False)


    def test_3_json_schema(self):
        _schema = generate_schema()
        f_out = open(os.path.join(Test_Resource_Dir, "../../../", "schema/resources.json"), "w")
        json.dump(obj=_schema, fp=f_out, sort_keys=True, indent=4)
        f_out.close()

        Draft4Validator.check_schema(_schema)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testDev']
    unittest.main()