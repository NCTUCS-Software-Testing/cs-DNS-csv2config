#! /usr/bin/env python3
# -*- coding:utf-8 -*-

import os
import csv
import time


OUTPUT_FILE = 'db.private_host'
DIR = 'host'
HOST_DMZ_10_1_0 = '0.host.csv'


def check_file_exit(filename, serial):
    new_filename = '{}.{}'.format(filename, serial)
    if os.path.isfile(new_filename):
        return new_filename
    else:
        new_filename = check_file_exit(filename, serial+1)
        return new_filename


def check_host_exit():
    if os.path.isfile(OUTPUT_FILE):
        localtime = time.localtime(time.time())
        init_filename = '{}.{}-{}-{}'.format(
            OUTPUT_FILE,
            localtime.tm_year, localtime.tm_mon, localtime.tm_mday)
        filename = check_file_exit(init_filename, 1):
        os.rename(OUTPUT_FILE, filename)
        return True
    else:
        return True


def open_csv_file_and_write(filename, write_file):
    with open(filename) as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            write_file.write(write_config_file(row))


def write_config_file(row):
    host = row[0].ljust(24)
    name_a = row[1]
    name_b = row[2]
    where = row[2]
    return '{}\t{}\t{}\t{}\n'.format(host, name_a, name_b, where)


def cover_csv_to_config():
    write_file = open(OUTPUT_FILE, mode="a+", encoding="utf-8")
    # cover DMZ (10.1.0.0/16)
    host_dmz = os.path.join(DIR, HOST_DMZ_10_1_0)
    if os.path.isfile(host_dmz):
        open_csv_file_and_write(host_dmz, write_file)
    # cover end
    write_file.close()


def main():
    cover_csv_to_config()


if __name__ == '__main__':
    main()
