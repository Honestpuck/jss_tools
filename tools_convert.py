#
# tools_convert.py
# some routines to take JSS data as strings and convert
# to python data types.
#
# v0.1
# *very* early version, mnore a proof of concept than anything real.
#

from time import strptime
from datetime import datetime

BOOL = 0
DATE = 1
INTN = 2
TIME = 3


def convert(dat):
    return {
        BOOL: lambda x: x == 'true',
        INTN: lambda x: int(x),
        DATE: lambda x: datetime.strptime(x, '%Y-%m-%d'),
        TIME: lambda x: strptime(x, '%Y-%m-%d %H:%M:%S'),
    }[dat[1]](dat[0])


_info_convert_keys = [
    ['id', BOOL],
    ['initial', DATE],
    ['last', TIME],
    ['managed', BOOL]
]


def info_convert(info):
    for cc in _info_convert_keys:
        info[cc[0]] = convert(cc)
    return info



