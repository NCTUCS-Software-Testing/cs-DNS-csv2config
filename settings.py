import os

DEBUGMODE = True
SOURCE_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'host')

# DMZ 10.1.0.0/24
DMZ_10_1_0 = ('0.host.csv', '0.rev')
# Core 10.1.1.0/24
CORE_10_1_1 = ('1.host.csv', '1.rev')
# Linux 10.1.2.0/24
LINUX_10_1_2 = ('2.host.csv', '2.rev')
# FreeBSD 10.1.3.0/24
BSD_10_1_3 = ('3.host.csv', '3.rev')
# WWW 10.1.4.0/24
WWW_10_1_4 = ('4.host.csv', '4.rev')
# Storage 10.1.5.0/24
STORAGE_10_1_5 = ('5.host.csv', '5.rev')
# VM 10.1.6.0/24
# == VM have two special DNS ==
VM_10_1_6 = ('6.host.csv', '6.rev')
# NET 10.1.7.0/24
NET_10_1_7 = ('7.host.csv', '7.rev')
# PC 10.1.8.0/24
PC_10_1_8 = ('8.host.csv', '8.rev')
# Mail 10.1.9.0/24
MAIL_10_1_9 = ('9.host.csv', '9.rev')


def debug_file_list(vm_domain):
    if vm_domain:
        file_list = [VM_10_1_6]
    else:
        file_list = [
            DMZ_10_1_0, CORE_10_1_1, LINUX_10_1_2, BSD_10_1_3, WWW_10_1_4,
            STORAGE_10_1_5, NET_10_1_7, PC_10_1_8, MAIL_10_1_9]
    return file_list


def debug_output_host(debug):
    if debug:
        return os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'working', 'db.private_host')
    else:
        return os.path.join(
            os.sep, 'etc', 'named', 'cc.cs', 'db.private_host')


def debug_output_dir(debug):
    if debug:
        return os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'working')
    else:
        return os.path.join(
            os.sep, 'etc', 'named', 'cc.cs')


def main():
    print(SOURCE_DIR)
    print(debug_output_host(DEBUGMODE))
    print(debug_output_dir(DEBUGMODE))
    print(debug_output_host(False))
    print(debug_output_dir(False))
    return True


if __name__ == '__main__':
    main()
