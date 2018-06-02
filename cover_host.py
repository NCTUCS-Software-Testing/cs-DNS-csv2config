#! /usr/bin/env python3
# -*- coding:utf-8 -*-

import os
import csv
import time


OUTPUT_HOST = 'db.private_host'
SOURCE_DIR = 'host'
OUTPUT_DIR = 'working'
# DMZ 10.1.0.0/24
HOST_DMZ_10_1_0 = '0.host.csv'
OUTPUT_0_REV = '0.rev'
# Core 10.1.1.0/24
HOST_CORE_10_1_1 = '1.host.csv'
OUTPUT_1_REV = '1.rev'
# Linux 10.1.2.0/24
HOST_LINUX_10_1_2 = '2.host.csv'
OUTPUT_2_REV = '2.rev'
# FreeBSD 10.1.3.0/24
HOST_BSD_10_1_3 = '3.host.csv'
OUTPUT_3_REV = '3.rev'
# WWW 10.1.4.0/24
HOST_WWW_10_1_4 = '4.host.csv'
OUTPUT_4_REV = '4.rev'
# Storage 10.1.5.0/24
HOST_WWW_10_1_4 = '5.host.csv'
OUTPUT_4_REV = '5.rev'
# VM 10.1.6.0/24
# == VM have two special DNS ==
# NET 10.1.7.0/24
HOST_WWW_10_1_4 = '7.host.csv'
OUTPUT_4_REV = '7.rev'
# PC 10.1.8.0/24
HOST_WWW_10_1_4 = '8.host.csv'
OUTPUT_4_REV = '8.rev'
# Mail 10.1.9.0/24
HOST_WWW_10_1_4 = '9.host.csv'
OUTPUT_4_REV = '9.rev'


def check_file_exist(filename, serial):
    new_filename = '{}.{}'.format(filename, serial)
    output_host_filename = os.path.join(OUTPUT_DIR, new_filename)
    if not os.path.isfile(output_host_filename):
        return new_filename
    else:
        new_filename = check_file_exit(filename, serial+1)
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
        #rename config and backup
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
    if data[3] is not '':
        name = data[0]
        where = data[1]
        host_a = data[2].ljust(24)
        host_b = data[3].ljust(24)
        return (
            '{}\tIN\t{}\t{}\n'.format(host_a, name, where),
            '{}\tIN\tcname\t{}\n'.format(host_b, where)
            )
    else:
        name = data[0]
        where = data[1]
        host_a = data[2].ljust(24)
        return (
            '{}\tIN\t{}\t{}\n'.format(host_a, name, where)
            )


def write_rev_config_file(data):
    ip = data[1].split('.')
    where = '{}.{}.{}.{}.in-addr.arpa.'.format(
        ip[3], ip[2], ip[1], ip[0]).ljust(28)
    host = data[2]
    return ('{}\tIN\tPTR\t{}\n'.format(where, host))


def cover_csv_to_config():
    output_host = check_host_exist(OUTPUT_HOST)
    write_file = open(output_host, mode="a+", encoding="utf-8")
    # cover DMZ (10.1.0.0/16)
    print("cover HOST DMZ (10.1.0.0/16)")
    host_csv = os.path.join(SOURCE_DIR, HOST_DMZ_10_1_0)
    if os.path.isfile(host_csv):
        open_csv_file_and_write_host(host_csv, write_file)
    # cover end
    write_file.close()


def cover_csv_to_rev():
    # cover DMZ (10.1.0.0/16)
    print("cover REV DMZ (10.1.0.0/16)")
    output_host = check_host_exist(OUTPUT_0_REV)
    write_file = open(output_host, mode="a+", encoding="utf-8")
    host_csv = os.path.join(SOURCE_DIR, HOST_DMZ_10_1_0)
    if os.path.isfile(host_csv):
        open_csv_file_and_write_rev(host_csv, write_file)
    write_file.close()
    # cover DMZ (10.1.0.0/16)


def check_init_exist():
    filename = os.path.join(SOURCE_DIR, HOST_DMZ_10_1_0)
    if os.path.isfile(filename):
        return True
    # check complete
    return False


def main():
    print("Cover CSV to DNS config")
    if check_init_exist():
        cover_csv_to_config()
        cover_csv_to_rev()
    else:
        print("Check init file exist")
    print("Cover CSV to DNS config complete")


if __name__ == '__main__':
    main()
