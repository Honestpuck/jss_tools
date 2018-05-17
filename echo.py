#
#
#
import time

with open('/Users/u398570/dev/jss_tools/XML/computer.xml') as f:
    for ln in f:
        print ln.rstrip()
        time.sleep(.075)


