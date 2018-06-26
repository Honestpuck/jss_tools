# example code

import jss_tools as tools
import sys

jss = tools.Jopen(True)


def printf(format, *args):
    sys.stdout.write(format % args)


def non_compliance(rec, reason):
    ''' might do something in here like email the malcontent but instead
    we'll just print something.'''
    computer = tools.info(rec)
    name = computer['realname']
    printf("%s\t%s", name, reason)


# old way
for computer in computer_list:
    this_computer = computer.retrieve()
    for attribute in this_computer.findall(
            'extension_attributes/extension_attribute'):
        # attributes for security compliance
        if attribute.findtext('name') == 'SIP status':
            if attribute.findtext('value') == 'disabled':
                o_non_comliance(this_computer, 'SIP status')
                break
        if attribute.findtext('name') == 'Virus Running':
            if attribute.findtext('value') in ['disabled', 'missing']:
                o_non_compliance(this_computer, 'Virus')
            break
        if attribute.findtext('name') == 'Internet Sharing':
            if attribute.findtext('value') == 'Enabled':
                o_non_compliance(this_computer, 'Internet Sharing')
            break

# new way
for record in computer_list:
    computer = record.retrieve()
    attribute = tools.attributes(computer)
    if attribute['SIP Status']['value'] == 'disabled':
        non_compliance(computer, 'SIP status')
        break
    if attribute['Virus Running']['value'] in ['disabled', 'missing']:
        non_compliance(computer, 'Virus')
        break
    if attribute['Internet Sharing']['value'] == 'Enabled':
        non_compliance(computer, 'Internet Sharing')
        break

# new way with EAs now supporting boolean types
for record in computer_list:
    computer = record.retrieve()
    attribute = tools.attributes(computer)
    if not attribute['SIP Disabled']['value']:
        non_compliance(computer, 'SIP status')
        break
    if not attribute['Virus Running']['value']:
        non_compliance(computer, 'Virus')
        break
    if not attribute['Internet Sharing Disabled']:
        non_compliance(computer, 'Internet Sharing')
        break

# more examples

# extract data from a smart group
c_group = tools.computergroup(jss.ComputerGroup(79))
for mac in c_group['computers']:
    ii = tools.c_info(jss.Computer(mac['id']))
    printf("User: %s Email: %s OS: %s Build: %s\n", ii['name'],
           ii['email'], ii['os'], ii['os_build'])

# check an attribute
for computer in jss.Computer():
    mac = computer.retrieve()
    attribs = tools.c_attributes(mac)
    if attribs['SIP status']['value'] == 'disabled':
        ii = tools.c_info(mac)
        printf("ID: %s User: %s Email: %s\n",
               ii['id'], ii['name'], ii['email'])
