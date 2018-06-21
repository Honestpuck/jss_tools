# example code

import jss_tools as tools
import sys


def printf(format, *args):
    sys.stdout.write(format % args)


def o_non_compliance(rec, reason):
    ''' might do something in here like email the malcontent but instead
    we'll just print something.'''
    name = rec.findtext('location/real_name')
    email = rec.findtext('location/email_address')
    mac_name = rec.findtext('general/name')
    printf("%s\t%s\t%s\t%s", name, email, mac_name, reason)


jss = tools.Jopen()

computer_list = jss.Computer()

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
        if attribute.findtext('name') == 'Carbon Black running':
            if attribute.findtext('value') in ['disabled', 'missing']:
                o_non_compliance(this_computer, 'Carbon Black')
            break
        if attribute.findtext('name') == 'Internet Sharing':
            if attribute.findtext('value') == 'Enabled':
                o_non_compliance(this_computer, 'Internet Sharing')
            break


def non_compliance(rec, reason):
    ''' might do something in here like email the malcontent but instead
    we'll just print something.'''
    computer = tools.info(rec)
    name = computer['realname']
    printf("%s\t%s", name, reason)


    # new way
    for record in computer_list:
        computer = record.retrieve()
        attribute = tools.attributes(computer)
        if attribute['SIP Status'] == 'disabled':
            non_compliance(computer, 'SIP status')
            break
        if attribute['Carbon Black Running'] in ['disabled', 'missing']:
            non_compliance(computer, 'Carbon Black')
            break
        if attribute['Internet Sharing'] == 'Enabled':
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
        if attribs['SIP status'] == 'disabled':
            ii = tools.c_info(mac)
            printf("ID: %s User: %s Email: %s\n",
                   ii['id'], ii['name'], ii['email'])
