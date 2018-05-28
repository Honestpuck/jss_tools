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

jss = tools.Jopen()

#
# COMPUTER RECORD
#

# get computer list
computers = jss.Computer()

# get one computer (417 is just a random number)
one_computer = jss.Computer('417')

# test info

info_A = tools.c_info(one_computer)
info_old = one_computer.find('general/serial_number').text

if info_A['serial'] == info_old:
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
    if nm == 'Self Service.app':
        apps_old_version = app.findtext('version')

if 'Chess' in apps_B:
    print "c_apps ignore: failed"
else:
    print "c_apps ignore: passed"

if (apps_A['Self Service'] == apps_B['Self Service']
        and apps_A['Self Service'] == apps_old_version):
    print "c_apps: passed"
else:
    print "c_apps: failed"


# test attributes
attrib = tools.c_attributes(one_computer)
attr_test_key = attrib.keys()[0]

for attr in one_computer.findall('extension_attributes/extension_attribute'):
    if attr.findtext('name') == attr_test_key:
        attr_val = attr.findtext('value')

if attrib[attr_test_key] == attr_val:
    print "c_attributes: passed"
else:
    print "c_attributes: failed"


# test users
u = tools.c_users(one_computer)
u_name = u[1]['name']
u_uid = u[1]['uid']

for usr in one_computer.find('groups_accounts/local_accounts'):
    if usr.findtext('name') == u_name:
        old_uid = usr.findtext('uid')

if old_uid == u_uid:
    print "c_users: passed"
else:
    print "c_users: failed"


# test certificates
c = tools.c_certificates(one_computer)[2]
common = c['common']
c_epoch = c['epoch']

for cert in one_computer.findall('certificates/certificate'):
    if cert.findtext('common_name') == common:
        old_epoch = cert.findtext('expires_epoch')

if c_epoch == old_epoch:
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

if old_name == pak['name']:
    print "package: passed"
else:
    print "package: failed"


# test policies
policies = jss.Policy()
pol_len = len(policies)
one_pol = jss.Policy(policies[randrange(pol_len)]['id'])
pol = tools.policy(one_pol)

old_name = one_pol.findtext('general/name')

if old_name == pol['name']:
    print "policy: passed"
else:
    print "policy: failed"

while pol['script_count'] == '0':
    one_pol = jss.Policy(policies[randrange(pol_len)]['id'])
    pol = tools.policy(one_pol)

sc_name = pol['scripts'][0]['name']
sc_priority = pol['scripts'][0]['priority']
for scr in one_pol.findall('scripts/script'):
    if scr.findtext('name') == sc_name:
        old_priority = scr.findtext('priority')
if old_priority == sc_priority:
    print "policy scripts: passed"
else:
    print "policy scripts: failed"

while pol['pak_count'] == '0':
    one_pol = jss.Policy(policies[randrange(pol_len)]['id'])
    pol = tools.policy(one_pol)

pak_name = pol['paks'][0]['name']
pak_id = pol['paks'][0]['id']
for pak in one_pol.findall('package_configuration/packages/package'):
    if pak.findtext('name') == pak_name:
        old_id = pak.findtext('id')
if old_id == pak_id:
    print "policy packages: passed"
else:
    print "policy packages: failed"


# test scripts
scripts = jss.Script()
one_script = jss.Script(scripts[2]['id'])
script = tools.script(one_script)

old_name = one_script.findtext('name')

if old_name == script['name']:
    print "script: passed"
else:
    print "script: failed"

# test computergroups

computergroups = jss.ComputerGroup()
c_group_len = len(computergroups)
one_c_group = jss.ComputerGroup(computergroups[randrange(c_group_len)]['id'])
c_group = tools.computergroup(one_c_group)

old_name = one_c_group.findtext('name')

if old_name == c_group['name']:
    print "computergroup: passed"
else:
    print "computergroup: failed"

while c_group['crit_count'] == '0':
    one_c_group = jss.ComputerGroup(
        computergroups[randrange(c_group_len)]['id'])
    c_group = tools.computergroup(one_c_group)

cg_name = c_group['criteria'][0]['name']
cg_value = c_group['criteria'][0]['value']
for cg in one_c_group.findall('criteria/criterion'):
    if cg.findtext('name') == cg_name:
        old_value = cg.findtext('value')
if old_value == cg_value:
    print "computergroup criteria: passed"
else:
    print "computergroup criteria: failed"

# test categories
categories = jss.Category()
one_cat = jss.Category(categories[5]['id'])
old_priority = one_cat.findtext('priority')
cat = tools.category(one_cat)

if int(old_priority) == cat['priority']:
    print "category: passed"
else:
    print "category: failed"
