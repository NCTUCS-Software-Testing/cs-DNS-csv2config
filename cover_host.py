#! /usr/bin/env python3
# -*- coding:utf-8 -*-

import os
import csv
import time

import settings

DEBUGMODE = True
VMDOMAIN = False

SOURCE_DIR = settings.SOURCE_DIR
OUTPUT_HOST = settings.debug_output_host(DEBUGMODE)
OUTPUT_DIR = settings.debug_output_dir(DEBUGMODE)
FILELIST = settings.debug_file_list(VMDOMAIN)


def check_file_exist(filename, serial):
    new_filename = '{}.{}'.format(filename, serial)
    output_host_filename = os.path.join(OUTPUT_DIR, new_filename)
    if not os.path.isfile(output_host_filename):
        return new_filename
    else:
        new_filename = check_file_exist(filename, serial+1)
        return new_filename


def check_host_exist(input_filename):
    output_host_filename = os.path.join(OUTPUT_DIR, input_filename)
    if os.path.isfile(output_host_filename):
        localtime = time.localtime(time.time())
        init_filename = '{}.{}-{}-{}'.format(
            input_filename,
            localtime.tm_year, localtime.tm_mon, localtime.tm_mday)
        filename = check_file_exist(init_filename, 1)
        new_output_host_filename = os.path.join(OUTPUT_DIR, filename)
        # rename config and backup
        os.rename(output_host_filename, new_output_host_filename)
        return output_host_filename
    else:
        return output_host_filename


def open_csv_file_and_write_host(filename, write_file):
    with open(filename) as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row_data in spamreader:
            write_to_file = write_host_config_file(row_data)
            for each_row in write_to_file:
                write_file.write(each_row)


def open_csv_file_and_write_rev(filename, write_file):
    with open(filename) as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row_data in spamreader:
            write_file.write(write_rev_config_file(row_data))


def write_host_config_file(data):
    if len(data) > 3 and data[3] is not '':
        name = data[0]
        where = data[1]
        host = data[2]
        re_tuple = ('{}\tIN\t{}\t{}\n'.format(host.ljust(24), name, where),)
        for host_cname in data[3:]:
            if host_cname is '':
                return re_tuple
            host_cname = host_cname.ljust(24)
            tmp_tuple = ('{}\tIN\tcname\t{}\n'.format(host_cname, host),)
            re_tuple = re_tuple + tmp_tuple
        return re_tuple
    else:
        name = data[0]
        where = data[1]
        host = data[2].ljust(24)
        return (
            '{}\tIN\t{}\t{}\n'.format(host, name, where)
            )


def write_rev_config_file(data):
    ip = data[1].split('.')
    where = '{}.{}.{}.{}.in-addr.arpa.'.format(
        ip[3], ip[2], ip[1], ip[0]).ljust(28)
    host = data[2]
    return ('{}\tIN\tPTR\t{}\n'.format(where, host))


def cover_csv_to_config(file_list):
    output_host = check_host_exist(OUTPUT_HOST)
    write_file = open(output_host, mode="a+", encoding="utf-8")
    # cover beging
    for each_file in file_list:
        print("  cover HOST {}\n".format(each_file[0]))
        host_csv = os.path.join(SOURCE_DIR, each_file[0])
        if os.path.isfile(host_csv):
            open_csv_file_and_write_host(host_csv, write_file)
        else:
            print("  cover HOST {} false, because file is not exist.".format(
                each_file[0])
                )
    # cover end
    write_file.close()


def cover_csv_to_rev(file_list):
    for each_file in file_list:
        print("  cover REV {}\n".format(each_file[0]))
        output_host = check_host_exist(each_file[1])
        write_file = open(output_host, mode="a+", encoding="utf-8")
        host_csv = os.path.join(SOURCE_DIR, each_file[0])
        if os.path.isfile(host_csv):
            open_csv_file_and_write_rev(host_csv, write_file)
        else:
            print("  cover HOST {} false, because file is not exist.".format(
                each_file[0])
                )
        write_file.close()


def check_init_exist(file_list):
    for each_file in file_list:
        filename = os.path.join(SOURCE_DIR, each_file[0])
        if not os.path.isfile(filename):
            print("  {} check file FAILE".format(each_file[0]))
            return False
    # check complete
    return True


def main():
    print("Cover CSV to DNS config")
    if check_init_exist(FILELIST):
        print("=========================================================")
        cover_csv_to_config(FILELIST)
        print("=========================================================")
        cover_csv_to_rev(FILELIST)
        print("=========================================================")
    else:
        print("  Check init file exist 'FALSE', please check!")
    print("Cover CSV to DNS config complete")


if __name__ == '__main__':
    main()
