#
# tools_convert.py
# some routines to take JSS data as strings and convert
# to python data types.
#
# v0.1
# *very* early version, mnore a proof of concept than anything real.
#

from datetime import datetime.strptime

BOOL = 0
DATE = 1
INTN = 2
TIME = 3


def convert(val, typ):
    return {
        BOOL: lambda x: x == 'true',
        INTN: lambda x: int(x),
        DATE: lambda x: strptime(x, '%Y-%m-%d'),
        TIME: lambda x: strptime(x, '%Y-%m-%d %H:%M:%S'),
    }[typ](val)


_info_convert_keys = [
    ['id', BOOL],
    ['initial', DATE],
    ['last', TIME],
    ['managed', BOOL],
    ['master', BOOL],
    ['mdm', BOOL],
    ['profiles_count', INTN]
]


def info_convert(info):
    for cc in _info_convert_keys:
        info[cc[0]] = convert(info[cc[0]], cc[1])
    return info
