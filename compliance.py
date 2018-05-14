#
# OS compliance
#

import jss_tools as t
import sys
from distutils.version import StrictVersion


def printf(format, *args):
    sys.stdout.write(format % args)
    sys.stdout.flush()


def non_compliance(info, reason):
    printf("%s\t%s\t%s\t%s\t%s-%s\n",
           info['machine_name'], info['name'], info['email'],
           reason, str(info['os']), str(info['os_build']))


def check_one(info):
    OS13BUILD = 97416
    OS12BUILD = 94067
    if StrictVersion(info['os']) < StrictVersion('10.12.6'):
        non_compliance(info, 'os_upgrade')
        return
    # 10.12.6 has two builds with 'G' :( Apple. Luckily both are compliant.
    if 'G' in info['os_build']:
        return
    if StrictVersion(info['os']) > StrictVersion('10.13.0') and (
            int(info['os_build'], 16) < OS13BUILD):
        non_compliance(info, 'os_update')
        return
    if (StrictVersion(info['os']) > StrictVersion('10.12.0')) and (
            int(info['os_build'], 16) < OS12BUILD):
        non_compliance(info, 'os_update')
        return


j = t.Jopen()

computer_list = j.Computer()

for computer in computer_list:
    this_computer = computer.retrieve()
    info = t.c_info(this_computer)
    check_one(info)

