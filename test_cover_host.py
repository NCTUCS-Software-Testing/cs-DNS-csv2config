#! /usr/bin/env python3
# -*- coding:utf-8 -*-

import unittest
import os
import time

from settings import DMZ_10_1_0
from settings import CORE_10_1_1
from settings import LINUX_10_1_2
from settings import BSD_10_1_3
from settings import WWW_10_1_4
from settings import STORAGE_10_1_5
from settings import VM_10_1_6
from settings import NET_10_1_7
from settings import PC_10_1_8
from settings import MAIL_10_1_9
from settings import debug_file_list
from settings import debug_output_host
from settings import debug_output_dir
from settings import main as settings_main

from cover_host import OUTPUT_HOST
from cover_host import OUTPUT_DIR
from cover_host import FILELIST
from cover_host import check_file_exist
from cover_host import check_host_exist
from cover_host import open_csv_file_and_write_host
from cover_host import open_csv_file_and_write_rev
from cover_host import write_host_config_file
from cover_host import write_rev_config_file
from cover_host import cover_csv_to_config
from cover_host import cover_csv_to_rev
from cover_host import check_init_exist
from cover_host import main as cover_host_main


class Test_cover_host(unittest.TestCase):
    """ Test settings.py """
    def test_debug_file_list(self):
        self.assertEqual([VM_10_1_6], debug_file_list(True))
        self.assertEqual(
            [
                DMZ_10_1_0, CORE_10_1_1, LINUX_10_1_2, BSD_10_1_3,
                WWW_10_1_4, STORAGE_10_1_5, NET_10_1_7, PC_10_1_8,
                MAIL_10_1_9
            ],
            debug_file_list(False)
        )

    def test_debug_output_host(self):
        self.assertEqual(os.path.join(
            os.path.dirname(
                os.path.abspath(__file__)), 'working', 'db.private_host'),
            debug_output_host(True)
        )
        self.assertEqual(os.path.join(
            os.sep,
            'etc', 'named', 'cc.cs', 'db.private_host'),
            debug_output_host(False)
        )

    def test_settings_main(self):
        self.assertTrue(settings_main())

    def test_debug_output_dir(self):
        self.assertEqual(os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'working'),
            debug_output_dir(True))
        self.assertEqual(os.path.join(
            os.sep, 'etc', 'named', 'cc.cs'),
            debug_output_dir(False))

    """ Test cover_host.py """
    def test_check_init_exist(self):
        """ Test check_init_exist(file_list) """
        self.assertEqual(
            True, check_init_exist(
                [
                    DMZ_10_1_0, CORE_10_1_1, LINUX_10_1_2, BSD_10_1_3,
                    WWW_10_1_4, STORAGE_10_1_5, NET_10_1_7, PC_10_1_8,
                    MAIL_10_1_9
                ]
            )
        )
        self.assertEqual(
            False, check_init_exist(
                [
                    ("Test1", "Test1.rev"),
                    ("Test2", "Test2.rev"),
                    ("Test3", "Test3.rev")
                ]
            )
        )

    def test_check_file_exist(self):
        file_list = [
            '0.rev', '1.rev', '2.rev', '3.rev', '4.rev',
            '5.rev', '6.rev', '7.rev', '8.rev', '9.rev'
        ]
        for each_file in file_list:
            self.assertEqual(each_file+".1", check_file_exist(each_file, 1))
        for each_file in file_list:
            f = open(os.path.join(OUTPUT_DIR, each_file+".1"), "w+")
            f.close()
            self.assertEqual(each_file+".2", check_file_exist(each_file, 1))
            os.remove(os.path.join(OUTPUT_DIR, each_file+".1"))

    def test_check_host_exist(self):
        file_list = [
            '0.rev', '1.rev', '2.rev', '3.rev', '4.rev',
            '5.rev', '6.rev', '7.rev', '8.rev', '9.rev'
            ]
        localtime = time.localtime(time.time())
        for each_file in file_list:
            self.assertEqual(
                os.path.join(OUTPUT_DIR, each_file),
                check_host_exist(each_file)
            )
        for each_file in file_list:
            f = open(os.path.join(OUTPUT_DIR, each_file), "w+")
            f.close()
            self.assertEqual(
                os.path.join(OUTPUT_DIR, each_file),
                check_host_exist(each_file)
            )
            os.remove(
                os.path.join(
                    OUTPUT_DIR, '{}.{}-{}-{}.1'.format(
                        each_file,
                        localtime.tm_year, localtime.tm_mon, localtime.tm_mday
                    )
                )
            )

    def test_cover_csv_to_config(self):
        os.mkdir(check_host_exist(OUTPUT_HOST))
        self.assertEqual(False, cover_csv_to_config(FILELIST))
        os.rmdir(check_host_exist(OUTPUT_HOST))
        self.assertEqual(True, cover_csv_to_config(FILELIST))

    def test_cover_csv_to_rev(self):
        os.mkdir(os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'working', '1.rev'))
        self.assertEqual(False, cover_csv_to_rev(FILELIST))
        os.rmdir(os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'working', '1.rev'))
        # self.assertEqual(True, cover_csv_to_config(FILELIST))

    def test_write_host_config_file(self):
        """ Normal A record """
        self.assertEqual(
            "test1".ljust(24)+"\tIN\tA\t10.0.0.1\n",
            write_host_config_file(["A", "10.0.0.1", "test1"])
        )
        """ One CNAME record """
        self.assertEqual(
            (
                "test1".ljust(24)+"\tIN\tA\t10.0.0.1\n",
                "cname1".ljust(24)+"\tIN\tcname\ttest1\n"
            ),
            write_host_config_file(["A", "10.0.0.1", "test1", "cname1"])
        )
        self.assertEqual(
            (
                "test1".ljust(24)+"\tIN\tA\t10.0.0.1\n",
                "cname1".ljust(24)+"\tIN\tcname\ttest1\n"
            ),
            write_host_config_file(["A", "10.0.0.1", "test1", 'cname1', ''])
        )
        """ Two CNAME record """
        self.assertEqual(
            (
                "test1".ljust(24)+"\tIN\tA\t10.0.0.1\n",
                "cname1".ljust(24)+"\tIN\tcname\ttest1\n",
                "cname2".ljust(24)+"\tIN\tcname\ttest1\n"
            ),
            write_host_config_file(
                ["A", "10.0.0.1", "test1", "cname1", "cname2"]))

    def test_write_rev_config_file(self):
        """ Nomal PTR record """
        self.assertEqual(
            "1.0.0.10.in-addr.arpa.".ljust(28)+"\tIN\tPTR\ttest1\n",
            write_rev_config_file(["A", "10.0.0.1", "test1"])
        )

    def test_cover_host_main(self):
        self.assertIsNone(cover_host_main())


if __name__ == "__main__":
    unittest.main()
