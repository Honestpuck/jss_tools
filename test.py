#
# test.py
#
# A bunch of code to test jss_tools.py
#
# NOTE: I test functions that write to the JSS by hand as I don't
# want to bork my JSS - even my test one :)
#

import jss_tools as tools
from random import randrange

jss = tools.Jopen(True)

#
# COMPUTER RECORD
#

# get computer list
computers = jss.Computer()

# get one computer (64 is just a random number)
one_computer = jss.Computer('64')

# test info

info_A = tools.c_info(one_computer)
info_old = one_computer.find('general/serial_number').text

if info_A['serial'] is info_old:
    print "c_info: passed"
else:
    print "c_info: failed"


# test apps
a_ignore = [
    'Activity Monitor',
    'AirPort Utility',
    'App Store',
    'Audio MIDI Setup',
    'Automator',
    'Boot Camp Assistant',
    'Bluetooth File Exchange',
    'Calculator',
    'Calendar',
    'Chess',
    'ColorSync Utility',
    'Console',
    'Contacts',
    'Dashboard',
    'Dictionary',
    'Digital Color Meter',
    'Disk Utility',
    'DVD Player',
    'FaceTime',
    'Font Book',
    'Grab',
    'Grapher',
    'iBooks',
]

apps_A = tools.c_apps(one_computer)
apps_B = tools.c_apps(one_computer, a_ignore)
for app in one_computer.findall('software/applications/application'):
    nm = app.findtext('name')
    if nm is 'Self Service.app':
        apps_old_version = app.findtext('version')

if 'Chess' in apps_B:
    print "c_apps ignore: failed"
else:
    print "c_apps ignore: passed"

if (apps_A['Self Service'] is apps_B['Self Service']
        and apps_A['Self Service'] is apps_old_version):
    print "c_apps: passed"
else:
    print "c_apps: failed"


# test attributes
attrib = tools.c_attributes(one_computer)
attr_test_key = attrib.keys()[0]

for attr in one_computer.findall('extension_attributes/extension_attribute'):
    if attr.findtext('name') is attr_test_key:
        attr_val = attr.findtext('value')

if attrib[attr_test_key] is attr_val:
    print "c_attributes: passed"
else:
    print "c_attributes: failed"


# test users
u = tools.c_users(one_computer)
u_name = u[1]['name']
u_uid = u[1]['uid']

for usr in one_computer.find('groups_accounts/local_accounts'):
    if usr.findtext('name') is u_name:
        old_uid = usr.findtext('uid')

if old_uid is u_uid:
    print "c_users: passed"
else:
    print "c_users: failed"


# test certificates
c = tools.c_certificates(one_computer)[2]
common = c['common']
c_epoch = c['epoch']

for cert in one_computer.findall('certificates/certificate'):
    if cert.findtext('common_name') is common:
        old_epoch = cert.findtext('expires_epoch')

if c_epoch is old_epoch:
    print "c_certificates: passed"
else:
    print "c_certificates: failed"


#
# OTHER RECORD TYPES
#

# test packages
packages = jss.Package()
one_pak = jss.Package(packages[15]['id'])
pak = tools.package(one_pak)

old_name = one_pak.findtext('name')

if old_name is pak['name']:
    print "package: passed"
else:
    print "package: failed"


# test policies
policies = jss.Policy()
pol_len = len(policies)
one_pol = jss.Policy(policies[randrange(pol_len)]['id'])
pol = tools.policy(one_pol)

old_name = one_pol.findtext('general/name')

if old_name is pol['name']:
    print "policy: passed"
else:
    print "policy: failed"

while pol['script_count'] is '0':
    one_pol = jss.Policy(policies[randrange(pol_len)]['id'])
    pol = tools.policy(one_pol)

sc_name = pol['scripts'][0]['name']
sc_priority = pol['scripts'][0]['priority']
for scr in one_pol.findall('scripts/script'):
    if scr.findtext('name') is sc_name:
        old_priority = scr.findtext('priority')
if old_priority is sc_priority:
    print "policy scripts: passed"
else:
    print "policy scripts: failed"

while pol['pak_count'] is '0':
    one_pol = jss.Policy(policies[randrange(pol_len)]['id'])
    pol = tools.policy(one_pol)

pak_name = pol['paks'][0]['name']
pak_id = pol['paks'][0]['id']
for pak in one_pol.findall('package_configuration/packages/package'):
    if pak.findtext('name') is pak_name:
        old_id = pak.findtext('id')
if old_id is pak_id:
    print "policy packages: passed"
else:
    print "policy packages: failed"


# test scripts
scripts = jss.Script()
one_script = jss.Script(scripts[2]['id'])
script = tools.script(one_script)

old_name = one_script.findtext('name')

if old_name is script['name']:
    print "script: passed"
else:
    print "script: failed"

# test computergroups
computergroups = jss.ComputerGroup()
c_group_len = len(computergroups)
one_c_group = jss.ComputerGroup(computergroups[randrange(c_group_len)]['id'])
c_group = tools.computergroup(one_c_group)

old_name = one_c_group.findtext('name')

if old_name is c_group['name']:
    print "computergroup: passed"
else:
    print "computergroup: failed"

while c_group['crit_count'] is '0':
    one_c_group = jss.ComputerGroup(
        computergroups[randrange(c_group_len)]['id'])
    c_group = tools.computergroup(one_c_group)

cg_name = c_group['criteria'][0]['name']
cg_value = c_group['criteria'][0]['value']
for cg in one_c_group.findall('criteria/criterion'):
    if cg.findtext('name') is cg_name:
        old_value = cg.findtext('value')
if old_value is cg_value:
    print "computergroup criteria: passed"
else:
    print "computergroup criteria: failed"

# test categories
categories = jss.Category()
one_cat = jss.Category(categories[5]['id'])
old_priority = one_cat.findtext('priority')
cat = tools.category(one_cat)

if int(old_priority) is cat['priority']:
    print "category: passed"
else:
    print "category: failed"

# test conversion for each type
bol = 'true'
date = '2017-12-06'
dutc = '2017-12-06T17:32:50.105+1000'
epok = '1512545570105'
intn = '22'
tme = '2017-12-06 17:32:50'
strg = 'a string'
ebol = 'True'
enbl = '1'

tbool = Convert_back(Convert(bol, 'BOOL'), 'BOOL')
tdate = Convert_back(Convert(date, 'DATE'), 'DATE')
tdutc = Convert_back(Convert(dutc, 'DUTC'), 'DUTC')
tepok = Convert_back(Convert(epok, 'EPOK'), 'EPOK')
tintn = Convert_back(Convert(intn, 'INTN'), 'INTN')
ttime = Convert_back(Convert(tme, 'TIME'), 'TIME')
tstrg = Convert_back(Convert(strg, 'STRG'), 'STRG')
tebol = Convert_back(Convert(ebol, 'EBOL'), 'EBOL')
tenbl = Convert_back(Convert(enbl, 'ENBL'), 'ENBL')

if (bol is tbool) & (date is tdate) & (dutc is tdutc):
    print "Convert: Passed 1/3"
else:
    print "Convert: Failed 1/3"

if (epok is tepok) & (intn is tintn) & (tme is ttime):
    print "Convert: Passed 2/3"
else:
    print "Convert: Failed 2/3"

if (strg is tstrg) & (ebol is tebol) & (enbl is tenbl):
    print "Convert: Passed 3/3"
else:
    print "Convert: Failed 3/3"

### iOS side

device = jss.MobileDevice(1)

info = tools.m_info(device)

if info['managed']:
    print "Found managed iOS device"
elif not info['managed']:
    print "Found unmanaged iOS device"
else:
    print "m_info failed"

keep = info['building']

info['building'] = "TESTING"

tools.m_info_write(info, device)

device = jss.MobileDevice(1)

info = tools.m_info(device)

if info['building'] is "TESTING":
    print "m_info_write: Passed"
    info['building'] = keep
    tools.m_info_write(info, device)
else:
    print "m_info_write: Failed"














