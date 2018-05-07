#
# test.py
#
# A bunch of code to test jss_tools.py
#

import jss_tools as tools

jss = tools.Jopen()

#
# COMPUTER RECORD
#

# get computer list
computers = jss.Computer()

# get one computer (22 is just a random number)
one_computer = jss.Computer(computers[22]['id'])

# test info
c_keys = [
    ['general/name', 'name'],
    ['general/mac_address', 'mac'],
    ['general/serial_number', 'serial'],
]

info_A = tools.info(one_computer)
info_B = tools.info(one_computer, c_keys)
info_old = one_computer.find('general/serial_number').text

if 'initial' in info_B:
    print "info keys: failed"
else:
    print "info keys: passed"

if info_A['serial'] == info_B['serial'] and info_B['serial'] == info_old:
    print "info: passed"

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
apps_A = tools.apps(one_computer)
apps_B = tools.apps(one_computer, a_ignore)
for app in one_computer.findall('software/applications/application'):
    nm = app.findtext('name')
    if nm == 'Self Service.app':
        apps_old_version = app.findtext('version')

if 'Chess' in apps_B:
    print "apps ignore: failed"
else:
    print "apps ignore: passed"

if (apps_A['Self Service'] == apps_B['Self Service']
        and apps_A['Self Service'] == apps_old_version):
    print "apps: passed"

# test attributes
attrib = tools.attributes(one_computer)
attr_test_key = attrib.keys()[-3]  # third from the end should be a name.

for attr in one_computer.findall('extension_attributes/extension_attribute'):
    if attr.findtext('name') == attr_test_key:
        attr_val = attr.findtext('value')

if attrib[attr_test_key] == attr_val:
    print "attributes: passed"

# test users
u = tools.users(one_computer)
u_name = u[1]['name']
u_uid = u[1]['uid']

for usr in one_computer.find('groups_accounts/local_accounts'):
    if usr.findtext('name') == u_name:
        old_uid = usr.findtext('uid')

if old_uid == u_uid:
    print "users: passed"

# test certificates
c = tools.certificates(one_computer)[2]
common = c['common']
c_epoch = c['epoch']

for cert in one_computer.findall('certificates/certificate'):
    if cert.findtext('common_name') == common:
        old_epoch = cert.findtext('expires_epoch')

if c_epoch == old_epoch:
    print "certificates: passed"

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

# test policies
policies = jss.Policy()
one_pol = jss.Policy(policies[3]['id'])
pol = tools.policy(one_pol)

old_name = one_pol.findtext('name')

if old_name == pol['name']:
    print "policy: passed"
