#
# sanitise a JSS by replacing any corporate data with random
# data
#

import jss_tools as tools
import random

jss = tools.Jopen(True)
surnames = []
for line in open('/Users/u398570/dev/bits/surnames.txt', 'r'):
    surnames.append(line.strip())
firsts = []
for line in open('/Users/u398570/dev/bits/first.txt', 'r'):
    firsts.append(line.strip())

for entry in jss.Computer():
    computer = entry.retrieve()
    info = tools.c_info(computer)
    surname = random.choice(surnames)
    first = random.choice(firsts)
    serial = info['serial']
    new_serial = ''.join(random.sample(serial, len(serial)))
    info['AD'] = 'int.corp.example'
    info['email'] = first + "." + surname.upper() + "@example.com"
    if 'MacBook' in info['model']:
        info['machine_name'] = "MB" + new_serial
    else:
        info['machine_name'] = "MD" + new_serial
    info['name'] = surname.upper() + ", " + first
    info['serial'] = new_serial
    info['user'] = first + surname[0]
    tools.c_info_write(info, computer)
