#
# tools_convert.py
# some routines to take JSS data as strings and convert
# to python data types.
#
# v0.1
# *very* early version, mnore a proof of concept than anything real.
#

from dateutil import parser
from datetime import datetime

BOOL = 0
DATE = 1  # plain date
DUTC = 2  # UTC date time and time zone 2018-01-09T19:44:55.000+1000
EPOK = 3  # Unix epoch
INTN = 4
TIME = 5  # date and time


def convert(val, typ):
    return {
        BOOL: lambda x: x == 'true',
        INTN: lambda x: int(x),
        DATE: lambda x: parser.parse(x),
        DUTC: lambda x: parser.parse(x),
        EPOK: lambda x: datetime.fromtimestamp(int(x)/1000)
        TIME: lambda x: parser.parse(x),
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
