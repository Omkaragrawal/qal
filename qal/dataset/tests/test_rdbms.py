"""
Created on Dec 17, 2013

@author: Nicklas Boerjesson
"""
import json

import unittest
import datetime
import os



from qal.common.listhelper import pretty_list
from qal.dataset.rdbms import RDBMSDataset
from qal.dataset.custom import DATASET_LOGLEVEL_DETAIL
from qal.common.resources import Resources
from qal.dal.dal import DatabaseAbstractionLayer
from qal.sql.macros import copy_to_table

Test_Script_Dir = os.path.dirname(__file__)
Test_Resource_Dir = Test_Script_Dir + '/resources'


class Test(unittest.TestCase):
    def test_1_Load_Save(self):
        """ Merge data from a PostgreSQL table into a MySQL table
        """
        _f_r = open(Test_Resource_Dir + "/resources.json", "r")
        _resources_list = json.load(_f_r)
        _resources = Resources(_resources_list=_resources_list, _base_path=Test_Resource_Dir)

        print("rdbms_test.test_1_Load_Save: Staging source")
        _source_data = [[1, 'source', datetime.datetime(2001, 1, 1, 0, 0)],
                        [2, 'source', datetime.datetime(2001, 1, 2, 0, 0)],
                        [3, 'source_new', datetime.datetime(2014, 1, 1, 0, 0)]]
        _field_names = ["ID", "Name", "Changed"]
        _field_types = ["integer", "string(200)", "datetime"]
        _source_dal = DatabaseAbstractionLayer(
            _resource=_resources["{1D62083E-88F7-4442-920D-0B6CC59BA2FF}"])

        _source_table_name = 'table_src'
        copy_to_table(_source_dal, _source_data, _field_names, _field_types, _source_table_name, _create_table=True,
                      _drop_existing=True)

        print("rdbms_test.test_1_Load_Save: Staging destination")
        _dest_data = [[1, 'dest', datetime.datetime(2001, 1, 1, 0, 0)],
                      [2, 'dest', datetime.datetime(2001, 1, 2, 0, 0)],
                      [3, 'dest', datetime.datetime(2014, 1, 4, 0, 0)]]

        _dest_dal = DatabaseAbstractionLayer(
            _resource=_resources["{DD34A233-47A6-4C16-A26F-195711B49B97}"])

        _dest_table_name = 'table_dst'
        copy_to_table(_dest_dal, _dest_data, _field_names, _field_types, _dest_table_name, _create_table=True,
                      _drop_existing=True)

        # Load source
        _d_source = RDBMSDataset(_resource=_resources["{1D62083E-88F7-4442-920D-0B6CC59BA2FF}"])
        _d_source.load()
        print("source:\n" + str(_d_source.data_table))

        # Load dest
        _d_dest = RDBMSDataset(_resource=_resources["{DD34A233-47A6-4C16-A26F-195711B49B97}"])
        _d_dest._log_level = DATASET_LOGLEVEL_DETAIL
        _d_dest.load()

        print("dest:\n" + str(_d_dest.data_table))

        _d_dest.apply_new_data(_new_data_table = _d_source.data_table, _key_fields=[2],
                               _insert=True, _update=True, _delete=True)

        _d_dest.save()
        _d_dest.load()

        print("log:\n" + pretty_list(_d_dest._log))

        # noinspection PyPep8
        _log_cmp = [
            'RDBMSDataset.delete;%5Bdatetime.datetime%282014%2C%201%2C%204%2C%200%2C%200%29%5D;%5B3%2C%20%27dest%27%2C%20datetime.datetime%282014%2C%201%2C%204%2C%200%2C%200%29%5D;Destination table: table_dst',
            'RDBMSDataset.insert;N/A%20in%20RDBMS;%5B3%2C%20%27source_new%27%2C%20datetime.datetime%282014%2C%201%2C%201%2C%200%2C%200%29%5D;Destination table: table_dst',
            'RDBMSDataset.update;1;;Name : dest =>source;Destination table: table_dst',
            'RDBMSDataset.update;0;;Name : dest =>source;Destination table: table_dst']
        self.assertEqual(_d_dest._log, _log_cmp, "Logs differ")

        print("result:\n" + str(_d_dest.data_table))

        self.assertEqual(_d_dest.data_table, [[1, 'source', datetime.datetime(2001, 1, 1, 0, 0)],
                                              [2, 'source', datetime.datetime(2001, 1, 2, 0, 0)],
                                              [3, 'source_new', datetime.datetime(2014, 1, 1, 0, 0)]], "Results differ")

        # TODO: Check if connections aren't garbage collected, are these needed?
        _d_source._dal.close()
        _d_dest._dal.close()


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()