#! /usr/bin/env python3
# -*- coding:utf-8 -*-

import unittest
from cover_host import *


class Test_cover_host(unittest.TestCase):
    """ Test cover_host.py """
    

    def test_check_init_exist(self):
        """ Test check_init_exist(file_list) """
        self.assertEqual(True, check_init_exist([DMZ_10_1_0, 
            CORE_10_1_1, LINUX_10_1_2, BSD_10_1_3, WWW_10_1_4,
            STORAGE_10_1_5, NET_10_1_7, PC_10_1_8, MAIL_10_1_9]))
        self.assertEqual(False, check_init_exist([("Test1", "Test1.rev")
        , ("Test2", "Test2.rev"), ("Test3", "Test3.rev")]))


    #def test_host_exist(self):
        

    #def test_file_exist(self):


    def test_write_host_config_file(self):
        """ Normal A record """
        self.assertEqual("test1".ljust(24)+"\tIN\tA\t10.0.0.1\n",
            write_host_config_file(["A", "10.0.0.1", "test1"]))
        """ One CNAME record """
        self.assertEqual(("test1".ljust(24)+"\tIN\tA\t10.0.0.1\n", 
            "cname1".ljust(24)+"\tIN\tcname\ttest1\n"), 
            write_host_config_file(["A", "10.0.0.1", "test1", "cname1"]))
        """ Two CNAME record """
        self.assertEqual((
            "test1".ljust(24)+"\tIN\tA\t10.0.0.1\n", 
            "cname1".ljust(24)+"\tIN\tcname\ttest1\n",
            "cname2".ljust(24)+"\tIN\tcname\ttest1\n"), 
            write_host_config_file(["A", "10.0.0.1", "test1", 
            "cname1", "cname2"]))


    def test_write_rev_config_file(self):
        """ Nomal PTR record """
        self.assertEqual("1.0.0.10.in-addr.arpa.".ljust(28)+
            "\tIN\tPTR\ttest1\n",
            write_rev_config_file(["A", "10.0.0.1", "test1"]))


if __name__ == "__main__":
    unittest.main()
